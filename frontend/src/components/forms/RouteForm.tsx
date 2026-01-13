import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Alert, AlertDescription } from "../ui/alert";
import { Loader2 } from "lucide-react";

const routeFormSchema = z.object({
  origin: z.string().min(1, "Origin address is required"),
  destination: z.string().min(1, "Destination address is required"),
  departureTime: z.string().optional(),
  arrivalTime: z.string().optional(),
}).refine(
  (data) => !(data.departureTime && data.arrivalTime),
  {
    message: "Provide either departure time or arrival time, not both",
    path: ["arrivalTime"],
  }
);

export type RouteFormData = z.infer<typeof routeFormSchema>;

interface RouteFormProps {
  onSubmit: (data: RouteFormData) => void;
  isLoading: boolean;
  error?: string | null;
}

export function RouteForm({ onSubmit, isLoading, error }: RouteFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RouteFormData>({
    resolver: zodResolver(routeFormSchema),
  });

  const departureTime = watch("departureTime");
  const arrivalTime = watch("arrivalTime");

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Calculate Commute</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="origin">Origin</Label>
            <Input
              id="origin"
              placeholder="Enter starting address"
              {...register("origin")}
            />
            {errors.origin && (
              <p className="text-sm text-destructive">{errors.origin.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="destination">Destination</Label>
            <Input
              id="destination"
              placeholder="Enter destination address"
              {...register("destination")}
            />
            {errors.destination && (
              <p className="text-sm text-destructive">{errors.destination.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="departureTime">Departure Time</Label>
              <Input
                id="departureTime"
                type="datetime-local"
                disabled={!!arrivalTime}
                {...register("departureTime")}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="arrivalTime">Arrival Time</Label>
              <Input
                id="arrivalTime"
                type="datetime-local"
                disabled={!!departureTime}
                {...register("arrivalTime")}
              />
            </div>
          </div>
          {errors.arrivalTime && (
            <p className="text-sm text-destructive">{errors.arrivalTime.message}</p>
          )}

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Calculating...
              </>
            ) : (
              "Calculate Route"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
