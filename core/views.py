from os import name
from django.shortcuts import render


testimonials = [
        {
            "id": 1,
            "name": "Yousuf Baloch",
            "role": "Customer",
            "image": "images/feedback-1.webp",
            "quote": "Adnan Baloch ke perfume ke quality aur lasting bohat behtareen hai...",
            "rating": 5
        },
        {
            "id": 2,
            "name": "Anas Baloch",
            "role": "Customer",
            "image": "images/feedback-2.webp",
            "quote": "Main important functions ke liye ek acha perfume dhund raha tha...",
            "rating": 4
        },
        {
            "id": 3,
            "name": "Meer Abdullah",
            "role": "Customer",
            "image": "images/feedback-3.webp",
            "quote": "It smells amazing, I really like it! I will definitely place another order...",
            "rating": 5
        },
    ]
products = [
    {
      "id": 1,
      "name": "Janan Sport",
      "brand": "J. Junaid Jamshed",
      "image": "/images/perfumes/janan-sport.jpeg",
      "description": "Janan Sport Perfume by Junaid Jamshed is a dynamic and energetic fragrance designed for the active, modern man.",
      "category": "Fresh"
    },
    {
      "id": 2,
      "name": "Lamsat Harir",
      "brand": "Arabiyat",
      "image": "/images/perfumes/lamsat-harir.jpeg",
      "description": "Lamsat Harir, meaning \"silk touch\" in Arabic, is a unisex fragrance by Arabiyat known for its sweet, fruity, and floral aroma.",
      "category": "Fresh"
    },
    {
      "id": 3,
      "name": "Mercedes Benz",
      "brand": "Mercedes-Benz",
      "image": "/images/perfumes/mercedes-benz.jpeg",
      "description": "Mercedes-Benz perfumes are designed to embody the brand's values of luxury, sophistication, and a modern, youthful energy.",
      "category": "Classic"
    },
    {
      "id": 4,
      "name": "Afnan's 9 PM",
      "brand": "Afnan",
      "image": "/images/perfumes/pm-9.jpeg",
      "description": "Afnan's 9 PM is a versatile, unisex fragrance known for its amber vanilla scent profile and is suitable for both daytime and evening wear.",
      "category": "Fresh"
    }
  ]

def home(request):

    context = {"testimonials": testimonials, "products": products}
    return render(request, 'core/home.html', context)

def about(request):
    context = {}
    return render(request, 'core/about.html', context)

def contact_us(request):
    context = {}
    return render(request, 'core/contact_us.html', context)