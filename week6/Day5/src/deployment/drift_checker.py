import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from scipy import stats

# Paths - use environment variables or defaults
TRAINING_DATA_PATH = os.getenv(
    "TRAINING_DATA_PATH", 
    "/home/prateek/Prateek/LaunchPad/week6/Day5/src/data/processed/final.csv"
)
PREDICTION_LOGS_PATH = os.getenv(
    "LOG_PATH", 
    "/home/prateek/Prateek/LaunchPad/week6/Day5/src/deployment/prediction_logs.csv"
)

# Feature columns to monitor
FEATURE_COLUMNS = ["Pclass", "Sex", "Age", "Embarked_S", "Embarked_C"]


class DriftChecker:
    def __init__(self, training_data_path: str = TRAINING_DATA_PATH):
        """Initialize with training data to establish baseline statistics."""
        self.training_data = pd.read_csv(training_data_path)
        self.baseline_stats = self._compute_baseline_stats()
        self.thresholds = self._set_thresholds()
        
    def _compute_baseline_stats(self) -> dict:
        """Compute baseline statistics from training data."""
        stats_dict = {}
        for col in FEATURE_COLUMNS:
            stats_dict[col] = {
                "mean": self.training_data[col].mean(),
                "std": self.training_data[col].std(),
                "min": self.training_data[col].min(),
                "max": self.training_data[col].max(),
                "median": self.training_data[col].median(),
                "q1": self.training_data[col].quantile(0.25),
                "q3": self.training_data[col].quantile(0.75),
            }
            # Add IQR for outlier detection
            iqr = stats_dict[col]["q3"] - stats_dict[col]["q1"]
            stats_dict[col]["lower_bound"] = stats_dict[col]["q1"] - 1.5 * iqr
            stats_dict[col]["upper_bound"] = stats_dict[col]["q3"] + 1.5 * iqr
        return stats_dict
    
    def _set_thresholds(self) -> dict:
        """Set thresholds for drift detection."""
        return {
            "psi_threshold": 0.2,  # Population Stability Index threshold
            "ks_p_value": 0.05,    # KS test p-value threshold
            "mean_shift_std": 2,   # Number of std devs for mean shift detection
        }
    
    def load_prediction_logs(self, hours: int = None) -> pd.DataFrame:
        """Load prediction logs, optionally filtered by time window."""
        if not os.path.exists(PREDICTION_LOGS_PATH):
            print(f"No prediction logs found at {PREDICTION_LOGS_PATH}")
            return pd.DataFrame()
        
        logs = pd.read_csv(PREDICTION_LOGS_PATH)
        
        if logs.empty:
            return logs
            
        if "timestamp" in logs.columns and hours:
            logs["timestamp"] = pd.to_datetime(logs["timestamp"])
            cutoff = datetime.now() - timedelta(hours=hours)
            logs = logs[logs["timestamp"] >= cutoff]
        
        return logs
    
    def detect_anomalies(self, data: pd.DataFrame) -> pd.DataFrame:
        """Detect anomalous individual predictions based on feature bounds."""
        if data.empty:
            return pd.DataFrame()
        
        anomalies = []
        for idx, row in data.iterrows():
            row_anomalies = []
            for col in FEATURE_COLUMNS:
                if col not in row:
                    continue
                value = row[col]
                baseline = self.baseline_stats[col]
                
                # Check if outside training data range
                if value < baseline["min"] or value > baseline["max"]:
                    row_anomalies.append({
                        "feature": col,
                        "value": value,
                        "issue": "outside_training_range",
                        "training_min": baseline["min"],
                        "training_max": baseline["max"]
                    })
                
                # Check if outlier based on IQR
                elif value < baseline["lower_bound"] or value > baseline["upper_bound"]:
                    row_anomalies.append({
                        "feature": col,
                        "value": value,
                        "issue": "statistical_outlier",
                        "lower_bound": baseline["lower_bound"],
                        "upper_bound": baseline["upper_bound"]
                    })
            
            if row_anomalies:
                anomalies.append({
                    "index": idx,
                    "timestamp": row.get("timestamp", "N/A"),
                    "anomalies": row_anomalies
                })
        
        return anomalies
    
    def calculate_psi(self, baseline: pd.Series, current: pd.Series, bins: int = 10) -> float:
        """Calculate Population Stability Index (PSI) between two distributions."""
        if len(current) < bins:
            return 0.0
        
        # Create bins based on baseline data
        _, bin_edges = np.histogram(baseline, bins=bins)
        
        # Calculate proportions for each bin
        baseline_counts, _ = np.histogram(baseline, bins=bin_edges)
        current_counts, _ = np.histogram(current, bins=bin_edges)
        
        # Add small value to avoid division by zero
        baseline_props = (baseline_counts + 0.001) / len(baseline)
        current_props = (current_counts + 0.001) / len(current)
        
        # Calculate PSI
        psi = np.sum((current_props - baseline_props) * np.log(current_props / baseline_props))
        return psi
    
    def detect_drift(self, prediction_logs: pd.DataFrame) -> dict:
        """Detect distribution drift between training data and prediction logs."""
        if prediction_logs.empty or len(prediction_logs) < 10:
            return {"status": "insufficient_data", "message": "Need at least 10 predictions to detect drift"}
        
        drift_results = {}
        
        for col in FEATURE_COLUMNS:
            if col not in prediction_logs.columns:
                continue
                
            baseline = self.training_data[col]
            current = prediction_logs[col]
            
            # Calculate PSI
            psi = self.calculate_psi(baseline, current)
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_pvalue = stats.ks_2samp(baseline, current)
            
            # Mean shift detection
            baseline_mean = self.baseline_stats[col]["mean"]
            baseline_std = self.baseline_stats[col]["std"]
            current_mean = current.mean()
            mean_shift_z = abs(current_mean - baseline_mean) / (baseline_std + 1e-10)
            
            # Determine drift status
            drift_detected = False
            reasons = []
            
            if psi > self.thresholds["psi_threshold"]:
                drift_detected = True
                reasons.append(f"PSI={psi:.4f} > {self.thresholds['psi_threshold']}")
            
            if ks_pvalue < self.thresholds["ks_p_value"]:
                drift_detected = True
                reasons.append(f"KS p-value={ks_pvalue:.4f} < {self.thresholds['ks_p_value']}")
            
            if mean_shift_z > self.thresholds["mean_shift_std"]:
                drift_detected = True
                reasons.append(f"Mean shift={mean_shift_z:.2f} std devs")
            
            drift_results[col] = {
                "drift_detected": drift_detected,
                "psi": round(psi, 4),
                "ks_statistic": round(ks_stat, 4),
                "ks_p_value": round(ks_pvalue, 4),
                "baseline_mean": round(baseline_mean, 4),
                "current_mean": round(current_mean, 4),
                "mean_shift_z": round(mean_shift_z, 4),
                "reasons": reasons if reasons else ["No drift detected"]
            }
        
        return drift_results
    
    def generate_report(self, hours: int = None) -> dict:
        """Generate a comprehensive drift and anomaly report."""
        print("=" * 60)
        print("DRIFT & ANOMALY DETECTION REPORT")
        print(f"Generated at: {datetime.now().isoformat()}")
        if hours:
            print(f"Time window: Last {hours} hours")
        print("=" * 60)
        
        # Load prediction logs
        logs = self.load_prediction_logs(hours)
        
        if logs.empty:
            print("\n⚠️  No prediction logs available for analysis.")
            return {"status": "no_data"}
        
        print(f"\n📊 Predictions analyzed: {len(logs)}")
        
        # Baseline statistics
        print("\n" + "-" * 40)
        print("BASELINE STATISTICS (Training Data)")
        print("-" * 40)
        for col in FEATURE_COLUMNS:
            stats = self.baseline_stats[col]
            print(f"\n{col}:")
            print(f"  Mean: {stats['mean']:.4f}, Std: {stats['std']:.4f}")
            print(f"  Range: [{stats['min']:.4f}, {stats['max']:.4f}]")
        
        # Drift detection
        print("\n" + "-" * 40)
        print("DRIFT DETECTION")
        print("-" * 40)
        drift_results = self.detect_drift(logs)
        
        if drift_results.get("status") == "insufficient_data":
            print(f"\n⚠️  {drift_results['message']}")
        else:
            any_drift = False
            for col, result in drift_results.items():
                status = "🔴 DRIFT" if result["drift_detected"] else "🟢 OK"
                any_drift = any_drift or result["drift_detected"]
                print(f"\n{col}: {status}")
                print(f"  PSI: {result['psi']}")
                print(f"  KS p-value: {result['ks_p_value']}")
                print(f"  Mean: {result['baseline_mean']} → {result['current_mean']}")
                if result["drift_detected"]:
                    print(f"  Reasons: {', '.join(result['reasons'])}")
            
            if not any_drift:
                print("\n✅ No significant drift detected in any feature.")
        
        # Anomaly detection
        print("\n" + "-" * 40)
        print("ANOMALY DETECTION")
        print("-" * 40)
        anomalies = self.detect_anomalies(logs)
        
        if not anomalies:
            print("\n✅ No anomalous predictions detected.")
        else:
            print(f"\n⚠️  Found {len(anomalies)} predictions with anomalies:")
            for anomaly in anomalies[:10]:  # Show first 10
                print(f"\n  Timestamp: {anomaly['timestamp']}")
                for a in anomaly["anomalies"]:
                    print(f"    - {a['feature']}: {a['value']} ({a['issue']})")
            
            if len(anomalies) > 10:
                print(f"\n  ... and {len(anomalies) - 10} more")
        
        print("\n" + "=" * 60)
        
        return {
            "total_predictions": len(logs),
            "drift_results": drift_results,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies
        }


def main():
    """Run drift checker as a standalone script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check for data drift and anomalies")
    parser.add_argument("--hours", type=int, help="Only analyze logs from the last N hours")
    args = parser.parse_args()
    
    checker = DriftChecker()
    checker.generate_report(hours=args.hours)


if __name__ == "__main__":
    main()
