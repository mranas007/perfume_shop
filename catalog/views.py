from django.shortcuts import render

products = [
  {
    "id": 1,
    "name": "After 12",
    "brand": "Al Haramain",
    "image": "images/perfumes/after-12.jpeg ",
    "description": "After 12 perfume is a fragrance known for its blend of fruity, sweet, and spicy notes, creating a captivating and intriguing scent.",
    "category": "Fresh"
  },
  {
    "id": 2,
    "name": "Bleu de Chanel",
    "brand": "Chanel",
    "image": "images/perfumes/bleu-de-chanel.jpeg",
    "description": "Bleu de Chanel is a woody aromatic fragrance for men, described as fresh, clean, and sensual, embodying independence and determination.",
    "category": "Woody"
  },
  {
    "id": 3,
    "name": "Blue Sea",
    "brand": "Fragrance World",
    "image": "/images/perfumes/blue-sea.jpeg",
    "description": "Blue Sea perfume is typically described as an aquatic fragrance, often associated with a refreshing, clean, and invigorating scent reminiscent of the sea and ocean breeze.",
    "category": "Fresh"
  },
  {
    "id": 4,
    "name": "COCO NOIR - CHANEL",
    "brand": "Chanel",
    "image": "/images/perfumes/coco-noir-chanel.jpeg",
    "description": "Chanel Coco Noir is a modern, luminous Oriental fragrance for women, described as an expression of magnetic sensuality.",
    "category": "Gourmand"
  },
  {
    "id": 5,
    "name": "Code by Diners",
    "brand": "Diners",
    "image": "/images/perfumes/code-diners.jpeg",
    "description": "Code by Diners is a bold and invigorating fragrance with a blend of citrus, spice, and woody notes.",
    "category": "Woody"
  },
  {
    "id": 6,
    "name": "Davidoff Cool Water",
    "brand": "Davidoff",
    "image": "/images/perfumes/davidoff-cool-water.jpeg",
    "description": "Davidoff Cool Water is a classic aromatic aquatic fragrance for men, known for its fresh and invigorating scent profile. It features top notes of sea water, lavender, and mint, creating a refreshing and clean opening.",
    "category": "Woody"
  },
  {
    "id": 7,
    "name": "Janan Gold Edition",
    "brand": "J. Junaid Jamshed",
    "image": "/images/perfumes/janan-gold-edition.jpeg",
    "description": "Janan Gold Edition, a fragrance by J. Junaid Jamshed, is a woody aromatic perfume for men, described as a perfect harmony of leather, chypre, and musk, revitalized by fruity notes.",
    "category": "Floral"
  },
  {
    "id": 8,
    "name": "Janan Intense",
    "brand": "J. Junaid Jamshed",
    "image": "/images/perfumes/janan-intense.jpeg",
    "description": "Janan Intense by J. is a bold and invigorating men's fragrance, characterized by its citrus-musky scent and a harmonious blend of notes.",
    "category": "Musk"
  },
  {
    "id": 9,
    "name": "Janan Sport",
    "brand": "J. Junaid Jamshed",
    "image": "/images/perfumes/janan-sport.jpeg",
    "description": "Janan Sport Perfume by Junaid Jamshed is a dynamic and energetic fragrance designed for the active, modern man.",
    "category": "Fresh"
  },
  {
    "id": 10,
    "name": "Lamsat Harir",
    "brand": "Arabiyat",
    "image": "/images/perfumes/lamsat-harir.jpeg",
    "description": "Lamsat Harir, meaning \"silk touch\" in Arabic, is a unisex fragrance by Arabiyat known for its sweet, fruity, and floral aroma.",
    "category": "Fresh"
  }
]
categories = ["All", "Fresh", "Classic", "Woody", "Floral", "Gourmand", "Musk"];

def catalog_page(request):

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'catalog/index.html', context)