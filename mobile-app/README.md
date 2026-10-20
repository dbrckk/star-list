# Freebuff Mobile — interface Android

Application mobile **locale** (PWA installable et APK WebView) pour piloter le client Freebuff sous Termux, sans PC. L'APK est une interface graphique : le moteur Freebuff ne se lance pas dans l'APK, mais dans Termux. **Fonctionne uniquement si Termux, les dépendances et le serveur local sont installés.** Les modèles Freebuff restent en ligne.

## Première installation — 1 commande dans Termux (Android ARM64)

1. Installer [Termux F-Droid](https://f-droid.org/packages/com.termux/).
2. Dans Termux :

```bash
pkg install -y curl && curl -fL https://raw.githubusercontent.com/dbrckk/star-list/freebuff-android/mobile-app/install-termux.sh -o ~/install-freebuff-mobile.sh && bash ~/install-freebuff-mobile.sh
```

Le script installe les composants, télécharge l'interface depuis ton dépôt et démarre un serveur local. Il demande explicitement une autorisation **avant** d'installer le port non officiel [LostSleepy/freebuff-android](https://github.com/LostSleepy/freebuff-android). Ce port n'a pas été audité ici et peut ne pas être compatible avec toutes les versions Android. Tu peux refuser et garder l'interface pour plus tard.

3. Ouvrir `http://127.0.0.1:8765` dans Chrome **ou installer l'APK** produit par GitHub Actions. Saisir le code d'appairage visible dans Termux. Tu peux ensuite « Ajouter à l'écran d'accueil » depuis Chrome pour obtenir une icône de lancement, même sans APK.
4. Ajouter un dépôt public `propriétaire/nom`, attendre son clonage, puis ouvrir le projet et utiliser l'agent Freebuff.

**Important :** pas de possibilité de cloner un dépôt privé depuis l'interface tant que l'authentification Git n'est pas configurée dans Termux. Aucune collecte de jetons GitHub dans l'interface. N'envoie jamais de code d'appairage à quelqu'un d'autre.

## Redémarrage et mises à jour

- Lancer : `~/.local/bin/freebuff-mobile-start`
- Arrêter : `~/.local/bin/freebuff-mobile-stop`
- Afficher le code d'appairage : `grep APPPAIRAGE ~/.freebuff-mobile/server.log` (pour une nouvelle session, redémarrer le serveur) ; plus précisément `grep 'CODE D.APPPAIRAGE' ~/.freebuff-mobile/server.log`.
- Mise à jour : relancer `bash ~/install-freebuff-mobile.sh` (réinstalle uniquement l'interface sans effacer les projets).
- Démarrage auto : installer [Termux:Boot](https://f-droid.org/packages/com.termux.boot/) et l'ouvrir une fois. Selon les réglages MIUI/HyperOS, autoriser les démarrages automatiques et exclure Termux des restrictions de batterie.

## Protection de données

Le serveur HTTP écoute uniquement `127.0.0.1`, et toutes les commandes sont protégées par jeton aléatoire de 256 bits et appairage 6 chiffres à usage unique (20 minutes, 8 essais maximum). L'accès à l'interface est local ; pas de serveur externe de contrôle. Le navigateur conserve localement le jeton. Les commandes côté serveur sont limitées (clone GitHub, démarrage session, texte, touches, arrêt session), sans exécution arbitraire d'arguments système depuis une URL ou un champ de formulaire. Les fichiers des projets restent sous `~/.freebuff-mobile/projects/`.

## Tests et compilation

```bash
node --test mobile-app/tests/server.test.js
```

Le workflow `.github/workflows/freebuff-mobile-apk.yml` compile l'APK Android avec Gradle sur GitHub Actions et publie un artifact `freebuff-mobile-debug-apk`, téléchargeable depuis Android sur la page du run GitHub. L'APK non signé pour le Play Store est une version **debug** à installer manuellement ; aucune publication Play Store n'est effectuée.
