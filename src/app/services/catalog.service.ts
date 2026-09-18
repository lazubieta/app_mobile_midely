import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, map, of, startWith, timeout } from 'rxjs';
import { environment } from '../../environments/environment';
import { Product } from '../models/product.interface';

interface ProductResponse {
  products: Product[];
}

const OFFLINE_PRODUCTS: Product[] = [
  {
    id: 101,
    title: 'Mochila urbana',
    description: 'Mochila resistente para trabajo, estudio y viajes cortos.',
    price: 89.9,
    category: 'accesorios',
    thumbnail: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80',
    rating: 4.8,
  },
  {
    id: 102,
    title: 'Audífonos inalámbricos',
    description: 'Sonido envolvente, estuche de carga y conexión Bluetooth.',
    price: 129.9,
    category: 'tecnología',
    thumbnail: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    rating: 4.6,
  },
  {
    id: 103,
    title: 'Camiseta esencial',
    description: 'Camiseta de algodón suave con corte clásico.',
    price: 49.9,
    category: 'moda',
    thumbnail: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
    rating: 4.7,
  },
  {
    id: 104,
    title: 'Vela aromática',
    description: 'Aroma de vainilla y madera para crear espacios acogedores.',
    price: 34.9,
    category: 'hogar',
    thumbnail: 'https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800&q=80',
    rating: 4.9,
  },
];

const SPANISH_CATEGORIES = new Set([
  'accesorios',
  'alimentos',
  'belleza',
  'deportes',
  'hogar',
  'moda',
  'tecnología',
  'tecnologia',
]);

@Injectable({ providedIn: 'root' })
export class CatalogService {
  private readonly http = inject(HttpClient);

  getProducts(): Observable<Product[]> {
    return this.http.get<ProductResponse>(`${environment.apiUrl}?limit=30`).pipe(
      timeout(6500),
      map((response) => {
        const apiProducts = response.products ?? [];
        const apiIsInSpanish = apiProducts.length > 0 && apiProducts.every((product) =>
          SPANISH_CATEGORIES.has(product.category.trim().toLowerCase()),
        );

        // La API es opcional para que la tienda también funcione sin conexión.
        // Si entrega categorías en otro idioma, se conserva el catálogo local en español.
        return apiIsInSpanish ? apiProducts : OFFLINE_PRODUCTS;
      }),
      startWith(OFFLINE_PRODUCTS),
      catchError(() => of(OFFLINE_PRODUCTS)),
    );
  }
}
