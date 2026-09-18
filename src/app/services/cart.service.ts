import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Preferences } from '@capacitor/preferences';
import { CartItem } from '../models/cart-item.interface';
import { Product } from '../models/product.interface';

@Injectable({ providedIn: 'root' })
export class CartService {
  private readonly storageKey = 'midely-cart';
  private readonly itemsSubject = new BehaviorSubject<CartItem[]>([]);
  private readonly totalSubject = new BehaviorSubject<number>(0);
  private readonly countSubject = new BehaviorSubject<number>(0);

  readonly items$ = this.itemsSubject.asObservable();
  readonly total$ = this.totalSubject.asObservable();
  readonly count$ = this.countSubject.asObservable();

  async load(): Promise<void> {
    const saved = await Preferences.get({ key: this.storageKey });
    try {
      const items = JSON.parse(saved.value ?? '[]') as CartItem[];
      this.setItems(Array.isArray(items) ? items : []);
    } catch {
      this.setItems([]);
    }
  }

  add(product: Product): void {
    const items = [...this.itemsSubject.value];
    const current = items.find((item) => item.product.id === product.id);
    if (current) {
      current.quantity += 1;
    } else {
      items.push({ product, quantity: 1 });
    }
    this.setItems(items);
    void this.persist();
  }

  increase(productId: number): void {
    const items = this.itemsSubject.value.map((item) =>
      item.product.id === productId ? { ...item, quantity: item.quantity + 1 } : item,
    );
    this.setItems(items);
    void this.persist();
  }

  decrease(productId: number): void {
    const items = this.itemsSubject.value
      .map((item) => item.product.id === productId ? { ...item, quantity: item.quantity - 1 } : item)
      .filter((item) => item.quantity > 0);
    this.setItems(items);
    void this.persist();
  }

  remove(productId: number): void {
    this.setItems(this.itemsSubject.value.filter((item) => item.product.id !== productId));
    void this.persist();
  }

  clear(): void {
    this.setItems([]);
    void this.persist();
  }

  private setItems(items: CartItem[]): void {
    this.itemsSubject.next(items);
    this.countSubject.next(items.reduce((total, item) => total + item.quantity, 0));
    this.totalSubject.next(items.reduce((total, item) => total + item.product.price * item.quantity, 0));
  }

  private async persist(): Promise<void> {
    await Preferences.set({ key: this.storageKey, value: JSON.stringify(this.itemsSubject.value) });
  }
}
