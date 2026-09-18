import { AsyncPipe, CurrencyPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import {
  IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonContent, IonHeader,
  IonIcon, IonImg, IonItem, IonLabel, IonList, IonNote, IonText, IonTitle, IonToolbar,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { add, cartOutline, checkmarkCircleOutline, remove, trashOutline } from 'ionicons/icons';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss'],
  imports: [AsyncPipe, CurrencyPipe, IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonContent, IonHeader, IonIcon, IonImg, IonItem, IonLabel, IonList, IonNote, IonText, IonTitle, IonToolbar],
})
export class Tab2Page {
  readonly cartService = inject(CartService);
  confirmationMessage = '';

  constructor() { addIcons({ add, cartOutline, checkmarkCircleOutline, remove, trashOutline }); }

  finishPurchase(): void {
    this.confirmationMessage = 'Pedido simulado confirmado. El carrito quedó listo para una nueva compra.';
    this.cartService.clear();
  }
}
