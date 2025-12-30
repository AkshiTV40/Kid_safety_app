"use client";

import { Capacitor } from '@capacitor/core';

export async function registerNativeFCM() {
  if (Capacitor.getPlatform() !== 'android' && Capacitor.getPlatform() !== 'ios') return null;
  try{
    // Import plugin dynamically so web builds don't break
    const mod: any = await import('@capacitor-firebase/messaging');
    const FirebaseMessaging = mod.FirebaseMessaging || mod;
    // request permissions (iOS) and get a token
    try{ await FirebaseMessaging.requestPermissions(); }catch(e){}
    let token = null;
    try{ const t = await FirebaseMessaging.getToken(); token = t.token || t; }catch(e){ console.warn('getToken failed', e); }
    // register a foreground listener
    try{ FirebaseMessaging.addListener && FirebaseMessaging.addListener('message', (m:any)=>{ console.log('native fcm message', m); }); }catch(e){}
    return token;
  }catch(e){
    console.warn('Native FCM plugin not available', e);
    return null;
  }
}
