package dev.freebuff.mobile;

import android.Manifest;
import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.content.Intent;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.provider.Settings;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceError;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.ScrollView;
import android.widget.Toast;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.atomic.AtomicBoolean;

/** Minimal Android host: the user-approved Termux service owns all project files. */
public class MainActivity extends Activity {
    private static final String ENDPOINT = "http://127.0.0.1:8765/";
    private static final String PERMISSION = "com.termux.permission.RUN_COMMAND";
    private static final String TERMUX_PACKAGE = "com.termux";
    private static final String TERMUX_SCRIPT = "/data/data/com.termux/files/home/.local/bin/freebuff-mobile-start";
    private static final String INSTALL = "pkg install -y curl && curl -fL https://raw.githubusercontent.com/dbrckk/star-list/freebuff-android/mobile-app/install-termux.sh -o ~/install-freebuff-mobile.sh && bash ~/install-freebuff-mobile.sh";
    private static final int REQUEST_TERMUX = 47;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final AtomicBoolean probing = new AtomicBoolean(false);
    private WebView browser;
    private LinearLayout root;
    private int retries = 0;
    private boolean automaticAttempted = false;
    private boolean waiting = false;
    private boolean destroyed = false;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(13,17,27));
        getWindow().setNavigationBarColor(Color.rgb(13,17,27));
        showConnecting("Connexion à ton espace de travail…");
        checkServer();
    }

    private GradientDrawable bg(int rgb){ GradientDrawable d=new GradientDrawable(); d.setColor(rgb); d.setCornerRadius(20); return d; }
    private TextView message(String s,int size,int color){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(color);t.setPadding(0,14,0,14);return t;}
    private void panel(String subtitle) {
        if(browser!=null){browser.stopLoading();browser.destroy();browser=null;}
        ScrollView scroll=new ScrollView(this);
        root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(38,44,38,32);
        root.setBackgroundColor(0xff0d111b);scroll.addView(root);setContentView(scroll);
        TextView title=message("Freebuff Mobile",30,0xff8bd6f6);title.setTypeface(null,Typeface.BOLD);root.addView(title);
        root.addView(message(subtitle,16,Color.WHITE));
    }
    private Button button(String label,Runnable action){
        Button b=new Button(this);b.setText(label);b.setTextColor(0xff0b2034);b.setAllCaps(false);
        b.setBackground(bg(0xff8bd6f6));b.setOnClickListener(v->action.run());
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2);p.setMargins(0,10,0,10);root.addView(b,p);return b;
    }
    private void showConnecting(String status){ panel(status); root.addView(message("Le service local sera relancé automatiquement lorsqu'Android l'autorise.",13,0xffaab9cd)); }
    private boolean hasTermux(){return getPackageManager().getLaunchIntentForPackage(TERMUX_PACKAGE)!=null;}
    private boolean hasPermission(){return checkSelfPermission(PERMISSION)==PackageManager.PERMISSION_GRANTED;}
    private void askPermission(){
        if (!hasTermux()){openExternal("https://f-droid.org/packages/com.termux/");return;}
        requestPermissions(new String[]{PERMISSION},REQUEST_TERMUX);
    }
    @Override public void onRequestPermissionsResult(int request,String[] names,int[] results){
        super.onRequestPermissionsResult(request,names,results);
        if(request==REQUEST_TERMUX){
            if(hasPermission()){retryStartup();}
            else {Toast.makeText(this,"Autorise les commandes Termux dans les paramètres de l'application",Toast.LENGTH_LONG).show();showHelp();}
        }
    }
    private void retryStartup(){ retries=0;automaticAttempted=false;showConnecting("Démarrage du service local…");checkServer(); }
    private void showHelp(){
        waiting=false;
        panel("Configuration nécessaire — une seule fois");
        if(!hasTermux()){
            root.addView(message("1. Installe Termux depuis F-Droid. Les versions de différentes boutiques ne sont pas toujours compatibles.",14,0xffaab9cd));
            button("Installer Termux",()->openExternal("https://f-droid.org/packages/com.termux/"));
        }else{
            root.addView(message("1. Ouvre Termux et colle la commande d'installation une seule fois. Elle configure le service, les dépendances et te demande l'accord pour le moteur communautaire non officiel.",14,0xffaab9cd));
            button("Copier la commande (installation initiale)",()->copy(INSTALL));
            button("Ouvrir Termux",()->{Intent i=getPackageManager().getLaunchIntentForPackage(TERMUX_PACKAGE);if(i!=null)startActivity(i);});
            root.addView(message("2. Pour permettre les démarrages suivants sans ouvrir Termux : autorise 'Exécuter des commandes dans Termux' pour Freebuff Mobile. L'installateur te propose aussi d'activer allow-external-apps dans Termux.",13,0xffaab9cd));
            if(!hasPermission())button("Autoriser le démarrage automatique",this::askPermission);
            button("Paramètres de Freebuff Mobile",()->{Intent i=new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,Uri.parse("package:"+getPackageName()));startActivity(i);});
            if(hasPermission())button("Démarrer le service",this::retryStartup);
        }
        button("Réessayer la connexion",this::retryStartup);
        root.addView(message("Les permissions Android nécessitent ton accord. Les projets restent dans Termux et Freebuff a toujours besoin d'Internet pour ses modèles.",12,0xff8495ac));
    }
    private void copy(String s){ClipboardManager m=(ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);m.setPrimaryClip(ClipData.newPlainText("Freebuff Mobile",s));Toast.makeText(this,"Commande copiée",Toast.LENGTH_SHORT).show();}
    private void openExternal(String url){startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}
    private boolean local(Uri u){return "http".equalsIgnoreCase(u.getScheme())&&"127.0.0.1".equals(u.getHost())&&u.getPort()==8765;}
    private void startTermuxService(){
        if(!hasTermux()||!hasPermission())return;
        try{
            Intent run=new Intent("com.termux.RUN_COMMAND");
            run.setClassName("com.termux","com.termux.app.RunCommandService");
            run.putExtra("com.termux.RUN_COMMAND_PATH",TERMUX_SCRIPT);
            run.putExtra("com.termux.RUN_COMMAND_WORKDIR","/data/data/com.termux/files/home");
            run.putExtra("com.termux.RUN_COMMAND_BACKGROUND",true);
            startService(run);
        }catch(Exception e){ /* Termux setting allow-external-apps may not yet be enabled. */ }
    }
    private void checkServer(){
        if(destroyed||browser!=null||!probing.compareAndSet(false,true))return;
        new Thread(()->{
            boolean ok=false;
            HttpURLConnection c=null;
            try{
                c=(HttpURLConnection)new URL(ENDPOINT).openConnection();
                c.setConnectTimeout(1000);c.setReadTimeout(1000);
                ok=c.getResponseCode()==200;
            }catch(Exception ignored){}finally{if(c!=null)c.disconnect();}
            final boolean alive=ok;
            runOnUiThread(()->{
                probing.set(false);
                if(destroyed||browser!=null)return;
                if(alive){waiting=false;showWeb();return;}
                if(!automaticAttempted&&hasTermux()&&hasPermission()){
                    automaticAttempted=true;waiting=true;startTermuxService();
                }
                if(waiting && retries++<10){handler.postDelayed(this::checkServer,1300);}
                else showHelp();
            });
        },"freebuff-connectivity").start();
    }
    private void showWeb(){
        browser=new WebView(this);browser.setBackgroundColor(0xff0d111b);
        WebSettings s=browser.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setJavaScriptCanOpenWindowsAutomatically(false);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);s.setSafeBrowsingEnabled(true);
        browser.setWebViewClient(new WebViewClient(){
            @Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest r){Uri u=r.getUrl();if(local(u))return false;if("https".equalsIgnoreCase(u.getScheme()))openExternal(u.toString());return true;}
            @Override public void onReceivedError(WebView v,WebResourceRequest req,WebResourceError err){if(req.isForMainFrame())runOnUiThread(()->{if(!destroyed&&browser==v){automaticAttempted=false;waiting=true;retries=0;showConnecting("Reconnexion au service…");checkServer();}});}
        });
        setContentView(browser);browser.loadUrl(ENDPOINT);
    }
    @Override public void onBackPressed(){if(browser!=null&&browser.canGoBack())browser.goBack();else super.onBackPressed();}
    @Override protected void onDestroy(){destroyed=true;handler.removeCallbacksAndMessages(null);if(browser!=null){browser.stopLoading();browser.destroy();browser=null;}super.onDestroy();}
}
