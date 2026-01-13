import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { MainLayout } from './components/layout/MainLayout';
import { RouteForm, RouteFormData } from './components/forms/RouteForm';
import { RouteResults } from './components/results/RouteResults';
import { routesApi } from './lib/api/routes';
import { RouteResponse } from './types/api';
import { Alert, AlertDescription, AlertTitle } from './components/ui/alert';
import { AlertCircle } from 'lucide-react';

function App() {
  const [routeData, setRouteData] = useState<RouteResponse | null>(null);
  const [targetArrivalTime, setTargetArrivalTime] = useState<string | undefined>();

  const mutation = useMutation({
    mutationFn: routesApi.calculate,
    onSuccess: (data) => {
      setRouteData(data);
    },
  });

  const handleSubmit = (data: RouteFormData) => {
    setTargetArrivalTime(data.arrivalTime);
    mutation.mutate({
      origin: data.origin,
      destination: data.destination,
      departure_time: data.departureTime ? new Date(data.departureTime).toISOString() : undefined,
      arrival_time: data.arrivalTime ? new Date(data.arrivalTime).toISOString() : undefined,
    });
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Plan Your Commute</h1>
          <p className="text-muted-foreground">
            Get accurate travel times and directions for your daily route.
          </p>
        </div>

        <RouteForm 
          onSubmit={handleSubmit} 
          isLoading={mutation.isPending}
          error={mutation.error ? (mutation.error as any).response?.data?.detail || mutation.error.message : null}
        />

        {mutation.isError && !mutation.error.message.includes("400") && (
           <Alert variant="destructive" className="max-w-md mx-auto">
             <AlertCircle className="h-4 w-4" />
             <AlertTitle>Error</AlertTitle>
             <AlertDescription>
               Something went wrong. Please try again later.
             </AlertDescription>
           </Alert>
        )}

        {routeData && routeData.routes.length > 0 && (
          <RouteResults 
            route={routeData.routes[0]} 
            targetArrivalTime={targetArrivalTime}
          />
        )}
      </div>
    </MainLayout>
  );
}

export default App;
