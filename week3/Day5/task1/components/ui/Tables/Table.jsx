import Tablehead from "./TableHead.jsx";
import TableRow from "./TableRow.jsx";

export default function Table({ data }) {
  return (
    <table className="w-full">
      <thead>
        <tr>
          {data.head.map((item, index) => (
            <Tablehead title={item} key={index} />
          ))}
        </tr>
      </thead>
      <tbody>
        {data.body.map((row, index) => (
          <TableRow key={index}>
            {row.map((elm, idx) => elm)}
          </TableRow>
        ))}
      </tbody>
    </table>
  );
}
