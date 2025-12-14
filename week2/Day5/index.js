const KEYWORDS = {
  all: [],

  men: [
    "mens-shirts",
    "mens-shoes",
    "mens-watches",
    "men's shirts",
    "men's t-shirts",
    "footwear",
    "athletic shoes",
    "sports cleats",
    "casual shoes",
    "watches",
    "leather watches",
    "luxury watches",
    // shared/unisex:
    "sunglasses",
    "sports-accessories",
    "mobile-accessories",
  ],

  women: [
    "tops",
    "womens-bags",
    "womens-dresses",
    "womens-jewellery",
    "womens-shoes",
    "womens-watches",
    // allow overlap into beauty/cosmetics:
    "beauty",
    "skin-care",
    "fragrances",
    "perfumes",
    "lipstick",
    "mascara",
    "eyeshadow",
    "face powder",
    "nail polish",
    // shared/unisex:
    "sunglasses",
    "sports-accessories",
    "mobile-accessories",
  ],

  kids: [
    // “usable by kids” (not necessarily labeled kids)
    "sports-accessories",
    "drinkware",
    "cups",
    "glasses",
    "dinnerware",
    "plates",
    "cutlery",
    "storage",
    "baking",
    "desserts",
    "beverages",
    // optional tech/accessories kids might use:
    "mobile-accessories",
    "wireless earphones",
    "over-ear headphones",
  ],

  accessories: [
    "accessories",
    "mobile-accessories",
    "sports-accessories",
    "kitchen-accessories",
    "sunglasses",
    "smartwatches",
    "wireless chargers",
    "chargers",
    "power banks",
    "phone accessories",
    "camera accessories",
    "selfie accessories",
    "wireless earphones",
    "over-ear headphones",
  ],

  cosmetics: [
    "beauty",
    "skin-care",
    "personal care",
    "fragrances",
    "perfumes",
    "mascara",
    "eyeshadow",
    "face powder",
    "lipstick",
    "nail polish",
    "hand soap",
    "body wash",
    "body lotion",
  ],
};

const api = "https://dummyjson.com/products?limit=500";

const navItems = document.querySelectorAll(".navItem");
const grid = document.getElementById("gridContainer");

const fetchProducts = async (apiUrl) => {
  try {
    const response = await fetch(apiUrl);
    const data = await response.json();
    return data.products ?? [];
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

const displayProducts = (products) => {
  grid.innerHTML = ""; 
  products.forEach((product) => {
    const div = document.createElement("div");
    div.classList.add("card");

    const img = document.createElement("img");
    img.src = product.thumbnail;

    const h3 = document.createElement("h3");
    h3.innerText = product.title;

    const span1 = document.createElement("span");
    span1.innerText = `rating: ${product.rating}`;

    const span2 = document.createElement("span");
    span2.innerText = `price: $${product.price}`;

    div.appendChild(img);
    div.appendChild(h3);
    div.appendChild(span1);
    div.appendChild(span2);

    grid.appendChild(div);
  });
};



const normalize = (s) => String(s ?? "").toLowerCase().trim();

const textPartsOfProduct = (p) => {
  const parts = [
    p?.category,
    p?.title,
    p?.description,
    ...(Array.isArray(p?.tags) ? p.tags : []),
    ...(Array.isArray(p?.brand) ? p.brand : [p?.brand]), // harmless if brand is string
  ];
  return parts.map(normalize).filter(Boolean);
};

const productMatchesKeywords = (product, keywords) => {
  if (!keywords || keywords.length === 0) return true; // "all"

  const haystack = textPartsOfProduct(product).join(" | ");
  return keywords.some((kw) => haystack.includes(normalize(kw)));
};

const filterProductsByGroup = (products, group) => {
  const keywords = KEYWORDS[group] ?? [];
  return products.filter((p) => productMatchesKeywords(p, keywords));
};

// helper: map nav label -> group key
const groupFromNavText = (txt) => {
  const t = normalize(txt).replace(/\s+/g, " ");
  if (t.startsWith("all")) return "all";
  if (t.startsWith("women's")) return "women";
  if (t.startsWith("men's")) return "men";
  if (t.startsWith("kids")) return "kids";
  if (t.startsWith("accessories")) return "accessories";
  if (t.startsWith("cosmetics")) return "cosmetics";
  return "all";
};

let allProducts = [];

const loadAll = async () => {
  allProducts = await fetchProducts(api);
  displayProducts(allProducts);
};

(() => {
  navItems[0].children[0].classList.add("underLine");

  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      navItems.forEach((Item) => Item.children[0].classList.remove("underLine"));
      item.children[0].classList.add("underLine");

      const group = groupFromNavText(item.innerText);

      if (group === "All") {
        displayProducts(allProducts);
        return;
      }

      const filteredProducts = filterProductsByGroup(allProducts, group);
      console.log({ group, count: filteredProducts.length, filteredProducts }); // “filtered products response”
      displayProducts(filteredProducts);
    });
  });
})();

loadAll(); 




