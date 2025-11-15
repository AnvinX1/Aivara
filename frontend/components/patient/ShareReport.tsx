"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import api from '@/lib/api';
import { Building2, User, Mail, Phone, MapPin, Loader2 } from 'lucide-react';

interface Hospital {
  id: number;
  name: string;
  address: string;
  city: string;
  state: string;
  pincode: string;
  phone?: string;
  email?: string;
}


interface Doctor {
  id: number;
  email: string;
  full_name?: string;
  specialization?: string;
  phone?: string;
  registration_number?: string;
}

interface ShareReportProps {
  reportId: number;
  reportName: string;
}

export function ShareReport({ reportId, reportName }: ShareReportProps) {
  const [open, setOpen] = useState(false);
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [selectedHospital, setSelectedHospital] = useState<number | null>(null);
  const [selectedDoctor, setSelectedDoctor] = useState<number | null>(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetchingHospitals, setFetchingHospitals] = useState(false);
  const [fetchingDoctors, setFetchingDoctors] = useState(false);
  const [cityFilter, setCityFilter] = useState('');
  const [stateFilter, setStateFilter] = useState('');

  useEffect(() => {
    if (open) {
      fetchHospitals();
    }
  }, [open, cityFilter, stateFilter]);

  useEffect(() => {
    if (selectedHospital) {
      fetchDoctors(selectedHospital);
    } else {
      setDoctors([]);
      setSelectedDoctor(null);
    }
  }, [selectedHospital]);

  const fetchHospitals = async () => {
    setFetchingHospitals(true);
    try {
      const data = await api.getHospitals(cityFilter || undefined, stateFilter || undefined);
      setHospitals(data);
    } catch (error: any) {
      toast.error('Failed to load hospitals', {
        description: error.response?.data?.detail || 'Please try again',
      });
    } finally {
      setFetchingHospitals(false);
    }
  };

  const fetchDoctors = async (hospitalId: number) => {
    setFetchingDoctors(true);
    try {
      const data = await api.getHospitalDoctors(hospitalId);
      setDoctors(data);
    } catch (error: any) {
      toast.error('Failed to load doctors', {
        description: error.response?.data?.detail || 'Please try again',
      });
    } finally {
      setFetchingDoctors(false);
    }
  };

  const handleShare = async () => {
    if (!selectedDoctor) {
      toast.error('Please select a doctor');
      return;
    }

    setLoading(true);
    try {
      await api.shareReportToDoctor(reportId, selectedDoctor, message || undefined);
      toast.success('Report shared successfully', {
        description: 'The doctor will be notified about your report',
      });
      setOpen(false);
      setSelectedHospital(null);
      setSelectedDoctor(null);
      setMessage('');
    } catch (error: any) {
      toast.error('Failed to share report', {
        description: error.response?.data?.detail || 'Please try again',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-full sm:w-auto">
          <User className="mr-2 h-4 w-4" />
          Share with Doctor
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Share Report with Doctor</DialogTitle>
          <DialogDescription>
            Select a hospital and doctor to share your report: <strong>{reportName}</strong>
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Filters */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="city">Filter by City (Optional)</Label>
              <Input
                id="city"
                placeholder="e.g., Mumbai, Delhi"
                value={cityFilter}
                onChange={(e) => setCityFilter(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="state">Filter by State (Optional)</Label>
              <Input
                id="state"
                placeholder="e.g., Maharashtra, Delhi"
                value={stateFilter}
                onChange={(e) => setStateFilter(e.target.value)}
              />
            </div>
          </div>

          {/* Hospital Selection */}
          <div>
            <Label>Select Hospital *</Label>
            {fetchingHospitals ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin" />
              </div>
            ) : (
              <Select
                value={selectedHospital?.toString() || ''}
                onValueChange={(value) => setSelectedHospital(parseInt(value))}
              >
                <SelectTrigger className="h-auto py-3">
                  <SelectValue placeholder="Choose a hospital">
                    {selectedHospital && hospitals.find(h => h.id === selectedHospital) && (
                      <div className="flex flex-col text-left">
                        <span className="font-semibold">
                          {hospitals.find(h => h.id === selectedHospital)?.name}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {hospitals.find(h => h.id === selectedHospital)?.city}, {hospitals.find(h => h.id === selectedHospital)?.state}
                        </span>
                      </div>
                    )}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  {hospitals.map((hospital) => (
                    <SelectItem key={hospital.id} value={hospital.id.toString()}>
                      <div className="flex flex-col">
                        <span className="font-semibold text-base">{hospital.name}</span>
                        <span className="text-sm text-muted-foreground">
                          {hospital.city}, {hospital.state} - {hospital.pincode}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          </div>

          {/* Doctor Selection */}
          {selectedHospital && (
            <div>
              <Label>Select Doctor *</Label>
              {fetchingDoctors ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin" />
                </div>
              ) : doctors.length === 0 ? (
                <div className="text-sm text-muted-foreground py-4">
                  No doctors available in this hospital
                </div>
              ) : (
                <div className="grid grid-cols-1 gap-3 max-h-64 overflow-y-auto">
                  {doctors.map((doctor) => (
                    <Card
                      key={doctor.id}
                      className={`cursor-pointer transition-all ${
                        selectedDoctor === doctor.id
                          ? 'ring-2 ring-primary border-primary'
                          : 'hover:border-primary/50'
                      }`}
                      onClick={() => setSelectedDoctor(doctor.id)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <User className="h-4 w-4 text-primary" />
                              <CardTitle className="text-lg">{doctor.full_name || doctor.email}</CardTitle>
                            </div>
                            {doctor.specialization && (
                              <Badge variant="secondary" className="mb-2">
                                {doctor.specialization}
                              </Badge>
                            )}
                            <div className="space-y-1 text-sm text-muted-foreground">
                              {doctor.phone && (
                                <div className="flex items-center gap-2">
                                  <Phone className="h-3 w-3" />
                                  <span>{doctor.phone}</span>
                                </div>
                              )}
                              <div className="flex items-center gap-2">
                                <Mail className="h-3 w-3" />
                                <span>{doctor.email}</span>
                              </div>
                              {doctor.registration_number && (
                                <div className="text-xs">Reg: {doctor.registration_number}</div>
                              )}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Message */}
          <div>
            <Label htmlFor="message">Message (Optional)</Label>
            <textarea
              id="message"
              className="w-full min-h-[100px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder="Add a message for the doctor..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleShare} disabled={!selectedDoctor || loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Sharing...
                </>
              ) : (
                <>
                  <User className="mr-2 h-4 w-4" />
                  Share Report
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

