# Freebuff Android — installation mobile

**Version 1.1.0.** Deux possibilités :

- **Android local sans PC** : télécharge [Freebuff-Android.sh](Freebuff-Android.sh) dans le dossier Téléchargements de ton téléphone. Installe [Termux (F-Droid)](https://f-droid.org/packages/com.termux/) puis exécute :
  ```bash
  termux-setup-storage
  bash ~/storage/downloads/Freebuff-Android.sh
  ```
  Le menu installe Ubuntu 24.04 avec PRoot, Node.js 22 ARM64 et le client CLI officiel Freebuff. Réparation sans suppression de projets : `~/.local/bin/freebuff-android --repair`. Tes dépôts restent dans `/root/projects` sous Ubuntu.
- **Codespaces dans Chrome** : [ouvrir directement un environnement Freebuff](https://codespaces.new/dbrckk/star-list/tree/freebuff-android), créer le Codespace, puis ouvrir un nouveau terminal et exécuter `freebuff-mobile`. Les dépôts sont séparés en dossiers `propriétaire__dépôt` sous `~/projects`.

Le navigateur Codespaces utilise un ordinateur Linux chez GitHub avec un quota gratuit, pas le processeur Android. La version Termux reste non validée sur appareil réel : le client Linux ARM64 peut rencontrer des incompatibilités PRoot. Aucune des deux méthodes ne garantit les quotas ou fonctionnalités graphiques de Freebuff Desktop.

Le code ne stocke pas de secrets et n'effectue aucun push automatique vers tes dépôts. **Ce n'est pas un contournement des restrictions des comptes Freebuff.**

## Vérifications

Exécute `bash .devcontainer/tests/test-shell.sh` à la racine du dépôt ; les tests utilisent des simulateurs locaux pour éviter d'utiliser des tokens. Le workflow CI tente aussi une installation effective de la CLI sur Ubuntu. Les tests simulés ne prouvent pas la compatibilité sur Android.
