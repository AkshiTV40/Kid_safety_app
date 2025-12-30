"use client";

import { Capacitor } from '@capacitor/core';

import { db } from './firebase';
import { ref, set } from 'firebase/database';

async function loadPlugin() {
  const pkg = '@capacitor' + '-firebase/messaging';
  try {
    const mod: any = await import(pkg);
    return mod.FirebaseMessaging || mod;
  } catch (e) {
    return null;
  }
}

export async function isNativeFCMAvailable(): Promise<boolean> {
  if (Capacitor.getPlatform() !== 'android' && Capacitor.getPlatform() !== 'ios') return false;
  const plugin = await loadPlugin();
  return !!plugin;
}

export async function registerNativeFCM(userId?: string) {
  if (Capacitor.getPlatform() !== 'android' && Capacitor.getPlatform() !== 'ios') return null;
  try{
    const FirebaseMessaging = await loadPlugin();
    if (!FirebaseMessaging) { console.warn('Native FCM plugin not available'); return null; }

    // request permissions (iOS) and get a token
    try{ await FirebaseMessaging.requestPermissions?.(); }catch(e){}
    let token = null;
    try{ const t = await FirebaseMessaging.getToken?.(); token = t?.token || t; }catch(e){ console.warn('getToken failed', e); }

    // store token in Realtime Database if userId provided
    if (token && userId) {
      try { await set(ref(db, `fcm_tokens/${userId}/${token}`), true); } catch(e){ console.warn('Failed to store native fcm token', e); }
    }

    // register a foreground listener
    try{ FirebaseMessaging.addListener && FirebaseMessaging.addListener('message', (m:any)=>{ console.log('native fcm message', m); }); }catch(e){}

    // token refresh
    try{ FirebaseMessaging.addListener && FirebaseMessaging.addListener('tokenRefresh', async (t:any)=>{
      const newToken = t?.token || t;
      if (newToken && userId) {
        try { await set(ref(db, `fcm_tokens/${userId}/${newToken}`), true); } catch(e){}
      }
    }); }catch(e){}

    return token;
  }catch(e){
    console.warn('Native FCM plugin error', e);
    return null;
  }
}
