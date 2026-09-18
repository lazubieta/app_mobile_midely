vi.mock('@capacitor/preferences', () => ({
  Preferences: {
    set: vi.fn().mockResolvedValue(undefined),
    get: vi.fn().mockResolvedValue({ value: null }),
  },
}));

import { Preferences } from '@capacitor/preferences';
import { TestBed } from '@angular/core/testing';
import { CartService } from './cart.service';
import { Product } from '../models/product.interface';

const product: Product = {
  id: 1,
  title: 'Producto de prueba',
  description: 'Producto para pruebas unitarias.',
  price: 25,
  category: 'pruebas',
  thumbnail: 'https://example.com/product.jpg',
};

describe('CartService', () => {
  let service: CartService;

  beforeEach(() => {
    vi.mocked(Preferences.set).mockClear();
    vi.mocked(Preferences.get).mockResolvedValue({ value: null });
    service = TestBed.inject(CartService);
  });

  it('adds products and calculates quantity and total', () => {
    service.add(product);
    service.add(product);
    let count = 0;
    let total = 0;
    service.count$.subscribe((value) => { count = value; }).unsubscribe();
    service.total$.subscribe((value) => { total = value; }).unsubscribe();
    expect(count).toBe(2);
    expect(total).toBe(50);
  });

  it('removes an item when its quantity reaches zero', () => {
    service.add(product);
    service.decrease(product.id);
    let currentItems = [] as unknown[];
    service.items$.subscribe((items) => { currentItems = items; }).unsubscribe();
    expect(currentItems).toHaveLength(0);
  });
});
