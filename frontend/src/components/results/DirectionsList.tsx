import { Route } from '../../types/api';
import { ScrollArea } from '../ui/scroll-area';
import { Separator } from '../ui/separator';
import { Badge } from '../ui/badge';
import { MapPin, Navigation } from 'lucide-react';

interface DirectionsListProps {
  route: Route;
}

export function DirectionsList({ route }: DirectionsListProps) {
  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-lg flex items-center gap-2">
          <Navigation className="h-5 w-5" />
          Turn-by-Turn Directions
        </h3>
        <Badge variant="secondary">
          {route.legs.reduce((acc, leg) => acc + leg.steps.length, 0)} steps
        </Badge>
      </div>
      
      <ScrollArea className="h-[400px] pr-4">
        <div className="space-y-6">
          {route.legs.map((leg, legIndex) => (
            <div key={legIndex} className="space-y-4">
              {legIndex > 0 && <Separator />}
              
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>Leg {legIndex + 1}</span>
              </div>

              <div className="space-y-4">
                {leg.steps.map((step, stepIndex) => (
                  <div key={stepIndex} className="flex gap-4 text-sm">
                    <div className="flex flex-col items-center">
                      <div className="h-2 w-2 rounded-full bg-primary mt-1.5" />
                      {stepIndex < leg.steps.length - 1 && (
                        <div className="w-[1px] bg-border flex-1 my-1" />
                      )}
                    </div>
                    <div className="flex-1 pb-4">
                      <div 
                        className="font-medium"
                        dangerouslySetInnerHTML={{ 
                          __html: step.navigationInstruction?.instructions || 'Proceed' 
                        }} 
                      />
                      <div className="text-muted-foreground text-xs mt-1">
                        {step.localizedValues?.staticDuration.text 
                          ? (step.localizedValues.staticDuration.text) 
                          : (step.staticDuration)} • {step.localizedValues?.distance?.text ?? `${step.distanceMeters}m`}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
