import { CurrencyPipe, TitleCasePipe } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  IonBadge, IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonCol,
  IonContent, IonGrid, IonHeader, IonIcon, IonImg, IonRow, IonSearchbar, IonSelect,
  IonSelectOption, IonSpinner, IonTitle, IonToolbar,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { cartOutline, refreshOutline, star } from 'ionicons/icons';
import { Product } from '../models/product.interface';
import { CatalogService } from '../services/catalog.service';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],
  imports: [CurrencyPipe, FormsModule, TitleCasePipe, IonBadge, IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonCol, IonContent, IonGrid, IonHeader, IonIcon, IonImg, IonRow, IonSearchbar, IonSelect, IonSelectOption, IonSpinner, IonTitle, IonToolbar],
})
export class Tab1Page implements OnInit {
  private readonly catalogService = inject(CatalogService);
  readonly cartService = inject(CartService);
  products: Product[] = [];
  filteredProducts: Product[] = [];
  categories: string[] = [];
  searchTerm = '';
  selectedCategory = 'todos';
  loading = true;
  errorMessage = '';
  readonly categorySelectOptions = { cssClass: 'category-popover', size: 'cover' as const };

  constructor() { addIcons({ cartOutline, refreshOutline, star }); }

  ngOnInit(): void { this.loadProducts(); }

  loadProducts(): void {
    this.loading = true;
    this.errorMessage = '';
    this.catalogService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.categories = [...new Set(products.map((product) => product.category))];
        this.filterProducts();
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'No fue posible cargar el catálogo. Intente nuevamente.';
        this.loading = false;
      },
    });
  }

  filterProducts(): void {
    const term = this.searchTerm.trim().toLowerCase();
    this.filteredProducts = this.products.filter((product) => {
      const matchesText = !term || `${product.title} ${product.description}`.toLowerCase().includes(term);
      const matchesCategory = this.selectedCategory === 'todos' || product.category === this.selectedCategory;
      return matchesText && matchesCategory;
    });
  }

  addToCart(product: Product): void { this.cartService.add(product); }
}
