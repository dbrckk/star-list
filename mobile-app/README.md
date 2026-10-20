# Freebuff Mobile — interface Android

Application mobile **locale** (PWA installable et APK WebView) pour piloter le client Freebuff sous Termux, sans PC. L'APK est une interface graphique : le moteur Freebuff ne se lance pas dans l'APK, mais dans Termux. **Fonctionne uniquement si Termux, les dépendances et le serveur local sont installés.** Les modèles Freebuff restent en ligne.

## Installation initiale (une seule fois)

1. Installe [l’APK de Freebuff Mobile](https://github.com/dbrckk/star-list/actions/workflows/freebuff-mobile-apk.yml) depuis les artefacts du dernier build validé. Il s'agit d'un APK debug : pas d'installation Play Store.
2. Installe [Termux depuis F-Droid](https://f-droid.org/packages/com.termux/).
3. Dans l’application, touche **Copier la commande**, puis ouvre Termux et colle-la. Le script télécharge les dépendances et l’interface, configure le service et propose deux consentements : autoriser le démarrage piloté par l'application et installer le port Freebuff Android **non officiel**. Sans ces consentements, le service peut être lancé manuellement et l'interface reste disponible.
4. Dans les paramètres Android de Freebuff Mobile, accorde si tu le souhaites « Exécuter des commandes dans Termux ». Reviens dans l'application : elle tentera de démarrer le service automatiquement à chaque ouverture. Le paramètre Termux `allow-external-apps=true` doit aussi avoir été accepté dans l'installation.
5. Saisis **une seule fois** le code d'appairage à six chiffres visible dans Termux. Il est conservé localement sur ton appareil via le stockage WebView. Ne partage pas ce code.

Pour le lancement facultatif au redémarrage du téléphone : installe [Termux:Boot](https://f-droid.org/packages/com.termux.boot/), ouvre-le une fois, puis autorise son exécution en arrière-plan si Android la bloque. L'installateur écrit déjà le script de démarrage.

## Utilisation quasi automatique

- Ouvre Freebuff Mobile depuis l'icône : l'APK tente de joindre le service et, si autorisé, de le redémarrer.
- Ajoute une fois `propriétaire/nom` : l'import Git est suivi automatiquement et le dépôt est ouvert quand il est prêt.
- Par défaut, Freebuff Mobile reprend ton dernier projet à l'ouverture. Cette option se désactive dans le tableau de bord.
- Les sessions de terminal persistent via tmux même si tu changes d'application. La connexion reste protégée par un jeton propre à ton téléphone.
- Les projets déjà présents ne sont pas effacés lors d'une mise à jour : le script télécharge d'abord les fichiers, vérifie leur syntaxe et les remplace seulement lorsque tout est disponible.
- Ni GitHub ni le moteur Freebuff ne reçoivent de modifications automatiques sans commande explicite de ta part. Les modèles restent en ligne et peuvent nécessiter un abonnement ou des quotas.

## Commandes de dépannage facultatives

- Relancer le serveur : `~/.local/bin/freebuff-mobile-start`
- Arrêter : `~/.local/bin/freebuff-mobile-stop`
- Réparer / mettre à jour : `bash ~/install-freebuff-mobile.sh`
- Diagnostic du port non officiel (si installé) : `freebuff android-doctor`

## Protection de données

Le serveur HTTP écoute uniquement `127.0.0.1`, et toutes les commandes sont protégées par jeton aléatoire de 256 bits et appairage 6 chiffres à usage unique (20 minutes, 8 essais maximum). L'accès à l'interface est local ; pas de serveur externe de contrôle. Le navigateur conserve localement le jeton. Les commandes côté serveur sont limitées (clone GitHub, démarrage session, texte, touches, arrêt session), sans exécution arbitraire d'arguments système depuis une URL ou un champ de formulaire. Les fichiers des projets restent sous `~/.freebuff-mobile/projects/`.

## Tests et compilation

```bash
node --test mobile-app/tests/server.test.js
```

Le workflow `.github/workflows/freebuff-mobile-apk.yml` compile l'APK Android avec Gradle sur GitHub Actions et publie un artifact `freebuff-mobile-debug-apk`, téléchargeable depuis Android sur la page du run GitHub. L'APK non signé pour le Play Store est une version **debug** à installer manuellement ; aucune publication Play Store n'est effectuée.
