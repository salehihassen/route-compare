import { GoogleMap, useJsApiLoader, Polyline, Marker } from '@react-google-maps/api';
import { Route } from '../../types/api';
import { useMemo, useState, useEffect } from 'react';
import { Skeleton } from '../ui/skeleton';

interface RouteMapProps {
  route: Route;
}

const containerStyle = {
  width: '100%',
  height: '400px',
  borderRadius: '0.5rem'
};

export function RouteMap({ route }: RouteMapProps) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '',
    libraries: ['geometry']
  });

  const [path, setPath] = useState<google.maps.LatLng[]>([]);

  useEffect(() => {
    if (isLoaded && route.polyline?.encodedPolyline && window.google) {
      const decodedPath = google.maps.geometry.encoding.decodePath(route.polyline.encodedPolyline);
      setPath(decodedPath);
    }
  }, [isLoaded, route]);

  const center = useMemo(() => {
    if (path.length === 0) return { lat: 0, lng: 0 };
    const lat = path.reduce((sum, p) => sum + p.lat(), 0) / path.length;
    const lng = path.reduce((sum, p) => sum + p.lng(), 0) / path.length;
    return { lat, lng };
  }, [path]);

  if (!isLoaded) return <Skeleton className="h-[400px] w-full" />;

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={(map) => {
        if (path.length > 0) {
            const bounds = new google.maps.LatLngBounds();
            path.forEach((p) => bounds.extend(p));
            map.fitBounds(bounds);
        }
      }}
    >
      {path.length > 0 && (
        <Polyline
          path={path}
          options={{
            strokeColor: "#2563eb",
            strokeOpacity: 1.0,
            strokeWeight: 4,
          }}
        />
      )}
      {path.length > 0 && (
        <>
          <Marker position={path[0]} label="A" />
          <Marker position={path[path.length - 1]} label="B" />
        </>
      )}
    </GoogleMap>
  );
}
