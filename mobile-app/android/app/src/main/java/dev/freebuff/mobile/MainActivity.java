package dev.freebuff.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
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

public class MainActivity extends Activity {
    private final String ENDPOINT = "http://127.0.0.1:8765/";
    private final String INSTALL = "pkg install -y curl && curl -fL https://raw.githubusercontent.com/dbrckk/star-list/freebuff-android/mobile-app/install-termux.sh -o ~/install-freebuff-mobile.sh && bash ~/install-freebuff-mobile.sh";
    private WebView browser;
    private LinearLayout root;
    @Override public void onCreate(Bundle state) { super.onCreate(state); getWindow().setStatusBarColor(Color.rgb(13,17,27)); getWindow().setNavigationBarColor(Color.rgb(13,17,27)); showWeb(); }
    private GradientDrawable bg(int rgb){GradientDrawable d=new GradientDrawable(); d.setColor(rgb); d.setCornerRadius(20); return d;}
    private TextView message(String s,int size,int color){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(color);t.setPadding(0,14,0,14);return t;}
    private Button button(String text,Runnable action){Button b=new Button(this);b.setText(text);b.setTextColor(0xff0b2034);b.setAllCaps(false);b.setBackground(bg(0xff8bd6f6));b.setOnClickListener(v->action.run());LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2);p.setMargins(0,10,0,10);root.addView(b,p);return b;}
    private void showHelp(){
       if(browser!=null){browser.destroy();browser=null;}
       ScrollView scroll=new ScrollView(this); root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(38,44,38,32);root.setBackgroundColor(0xff0d111b);scroll.addView(root);setContentView(scroll);
       TextView title=message("Freebuff Mobile",30,0xff8bd6f6);title.setTypeface(null,Typeface.BOLD);root.addView(title);
       root.addView(message("Le moteur local n'est pas encore actif.",18,Color.WHITE));
       root.addView(message("1. Installe Termux depuis F-Droid.\n2. Ouvre Termux et colle la commande d'installation.\n3. Reviens ici et touche Réessayer.\n\nLa première installation demande ton autorisation avant d'utiliser un port Freebuff non officiel.",15,0xffaab9cd));
       button("Copier la commande d'installation",()->{ClipboardManager m=(ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);m.setPrimaryClip(ClipData.newPlainText("Installer Freebuff Mobile",INSTALL));Toast.makeText(this,"Commande copiée",Toast.LENGTH_SHORT).show();});
       button("Ouvrir Termux",()->{Intent i=getPackageManager().getLaunchIntentForPackage("com.termux");if(i!=null)startActivity(i);else openExternal("https://f-droid.org/packages/com.termux/");});
       button("Réessayer",this::showWeb);
       root.addView(message("Le service écoute uniquement sur 127.0.0.1. Aucun serveur cloud n'est nécessaire pour l'interface. Les modèles IA nécessitent Internet.",12,0xff8495ac));
    }
    private void openExternal(String address){startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(address)));}
    private boolean local(Uri uri){return "http".equalsIgnoreCase(uri.getScheme())&&"127.0.0.1".equals(uri.getHost())&&uri.getPort()==8765;}
    private void showWeb(){
      browser=new WebView(this); browser.setBackgroundColor(0xff0d111b);
      WebSettings s=browser.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setJavaScriptCanOpenWindowsAutomatically(false);s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW); s.setSafeBrowsingEnabled(true);
      browser.setWebViewClient(new WebViewClient(){
          @Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest r){Uri u=r.getUrl();if(local(u))return false;if("https".equalsIgnoreCase(u.getScheme()))openExternal(u.toString());return true;}
          @Override public void onReceivedError(WebView v,WebResourceRequest req,WebResourceError err){if(req.isForMainFrame()) runOnUiThread(()->showHelp());}
      });
      setContentView(browser);browser.loadUrl(ENDPOINT);
    }
    @Override public void onBackPressed(){if(browser!=null&&browser.canGoBack())browser.goBack();else super.onBackPressed();}
    @Override protected void onDestroy(){if(browser!=null)browser.destroy();super.onDestroy();}
}
