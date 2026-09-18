import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonContent, IonHeader,
  IonIcon, IonInput, IonItem, IonLabel, IonNote, IonText, IonTitle, IonToolbar,
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { logInOutline, logOutOutline, shieldCheckmarkOutline } from 'ionicons/icons';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss'],
  imports: [AsyncPipe, FormsModule, IonButton, IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonContent, IonHeader, IonIcon, IonInput, IonItem, IonLabel, IonNote, IonText, IonTitle, IonToolbar],
})
export class Tab3Page {
  readonly authService = inject(AuthService);
  email = 'demo@midely.com';
  password = 'midely123';
  message = '';
  error = false;
  submitting = false;

  constructor() { addIcons({ logInOutline, logOutOutline, shieldCheckmarkOutline }); }

  async login(): Promise<void> {
    this.submitting = true;
    this.message = '';
    const result = await this.authService.login(this.email, this.password);
    this.error = !result.ok;
    this.message = result.message;
    this.submitting = false;
  }

  async logout(): Promise<void> { await this.authService.logout(); }
}
