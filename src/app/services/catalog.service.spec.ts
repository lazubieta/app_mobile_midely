import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { CatalogService } from './catalog.service';
import { environment } from '../../environments/environment';

describe('CatalogService', () => {
  let service: CatalogService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [CatalogService, provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(CatalogService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('maps the API response to the product list', () => {
    const products = [{ id: 1, title: 'Producto', price: 10, description: 'Descripción', category: 'hogar', thumbnail: 'image' }];
    const results: unknown[] = [];
    service.getProducts().subscribe((result) => results.push(result));
    const request = http.expectOne(`${environment.apiUrl}?limit=30`);
    expect(request.request.method).toBe('GET');
    request.flush({ products });
    expect(results).toHaveLength(2);
    expect(results[1]).toEqual(products);
  });
});
