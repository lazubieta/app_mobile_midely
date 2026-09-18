# Midely

Midely es una tienda móvil híbrida construida con Ionic, Angular y Capacitor. El proyecto incluye catálogo conectado a API, autenticación de demostración, carrito de compras y persistencia local.

## Ejecución

```powershell
pnpm install
pnpm start
```

## Validación

```powershell
pnpm build
pnpm lint
pnpm test --no-watch --no-progress
pnpm exec cap sync android
pnpm exec cap add ios
```

Para Android, se puede abrir `android` en Android Studio y ejecutar el emulador o un dispositivo conectado. Para iOS se requiere macOS con Xcode; el proyecto nativo está en `ios/App`.

## Funcionalidades

- Catálogo consumido desde DummyJSON con productos de respaldo para modo sin conexión.
- Filtros por texto y categoría.
- Carrito con incremento, decremento, eliminación y confirmación de pedido demostrativa.
- Sesión de autenticación local con validación de correo y contraseña.
- Persistencia del carrito y la sesión mediante `@capacitor/preferences`.
- Suite de pruebas para catálogo, carrito y autenticación.

## Seguridad y lanzamiento

La contraseña nunca se persiste: únicamente se guarda una sesión mínima de demostración. Para producción se debe reemplazar `AuthService` por un proveedor de identidad con tokens de corta duración, HTTPS, gestión de secretos fuera del repositorio, validación del servidor y política de privacidad.

Antes de publicar se debe generar una compilación release firmada, revisar permisos, actualizar el número de versión, probar en dispositivos físicos y completar las fichas de Google Play Console y App Store Connect. La publicación en las tiendas requiere las membresías correspondientes.
