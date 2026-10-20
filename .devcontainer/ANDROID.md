# Freebuff Android — installation mobile

**Version 1.3.0.** Deux possibilités :

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

## Corrections 1.2
- Script Termux : corrections des sauts de ligne et répertoires `owner__repo`, pour ne pas confondre deux dépôts portant le même nom.
- GitHub Actions : tests de syntaxe et simulation Termux, plus installation CLI sur Linux ARM64 natif (`ubuntu-24.04-arm`) et x86-64. Voir l’onglet Actions pour leur résultat.
- Pour diagnostiquer une panne sur Android : `~/.local/bin/freebuff-android --diagnostic`.
- Les tests Linux ARM64 **ne remplacent pas** un test Android 15 dans PRoot ; ne pas annoncer que l’application fonctionne sur le téléphone tant que cela n’a pas été vérifié.
- L’installateur reste accessible directement ici : [Freebuff-Android.sh](Freebuff-Android.sh).

## Nouveautés 1.3.0

- Avant la première installation, vérification d'au moins 1,5 Gio disponibles (le besoin réel peut varier).
- `bash Freebuff-Android.sh --doctor` effectue un diagnostic local sans envoyer de logs, clés, identifiants ni contenu de dépôt.
- Test CI supplémentaire du **démarrage interactif** de Freebuff CLI avec un pseudo-terminal, sur Linux x64 et ARM64. Ce test détecte les régressions de démarrage qui passent `--version` mais n'ouvrent pas Freebuff.
- La réussite du CI Linux ne prouve pas encore le fonctionnement sur Android 15/PRoot.

**Mise à niveau sur Termux :** télécharger le nouvel installateur puis exécuter
`bash ~/storage/downloads/Freebuff-Android.sh --repair`.
Ne pas supprimer Ubuntu/PRoot : les fichiers et identifiants de session existants sont conservés lors de la réparation.
