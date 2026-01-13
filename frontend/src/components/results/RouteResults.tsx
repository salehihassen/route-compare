import { Route } from '../../types/api';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { RouteMap } from './RouteMap';
import { DirectionsList } from './DirectionsList';
import { Clock, MapPin, Calendar } from 'lucide-react';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription, AlertTitle } from '../ui/alert';

interface RouteResultsProps {
  route: Route;
  targetArrivalTime?: string;
}

export function RouteResults({ route, targetArrivalTime }: RouteResultsProps) {
  // Calculate recommended departure if target arrival time is set
  const recommendedDeparture = targetArrivalTime ? (() => {
    const arrival = new Date(targetArrivalTime);
    const durationSeconds = parseInt(route.duration.replace('s', ''));
    const departure = new Date(arrival.getTime() - durationSeconds * 1000);
    return departure;
  })() : null;

  const isLate = recommendedDeparture && recommendedDeparture < new Date();

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {recommendedDeparture && (
        <Alert variant={isLate ? "destructive" : "default"} className="mb-6">
          <Clock className="h-4 w-4" />
          <AlertTitle>Smart Schedule</AlertTitle>
          <AlertDescription>
            To arrive by {new Date(targetArrivalTime!).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}, 
            you should depart by <span className="font-bold">{recommendedDeparture.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>.
            {isLate && " You are running late!"}
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Route Summary</span>
              <Badge variant="outline" className="text-lg px-3 py-1">
                {route.localizedValues.duration.text}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2 text-muted-foreground">
              <MapPin className="h-4 w-4" />
              <span>{route.localizedValues.distance.text}</span>
            </div>
            
            <div className="rounded-lg overflow-hidden border">
              <RouteMap route={route} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <DirectionsList route={route} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
