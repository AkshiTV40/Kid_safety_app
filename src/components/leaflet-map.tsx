"use client";

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default function LeafletMap({ center = [0,0], zoom = 13, marker }: { center?: [number,number], zoom?: number, marker?: {lat:number,lng:number} | null }){
  const ref = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  useEffect(()=>{
    if (!ref.current) return;
    if (!mapRef.current){
      mapRef.current = L.map(ref.current).setView(center as [number,number], zoom);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(mapRef.current);
    }
    // remove previous marker layers
    mapRef.current!.eachLayer((layer) => {
      try { if ((layer as any)._icon) (mapRef.current as any).removeLayer(layer); } catch(e){}
    });
    if (marker && mapRef.current){
      const m = L.marker([marker.lat, marker.lng]).addTo(mapRef.current);
      mapRef.current.setView([marker.lat, marker.lng]);
    }
  }, [ref, marker]);

  return <div ref={ref} style={{height: '400px'}} className="rounded overflow-hidden" />;
}
