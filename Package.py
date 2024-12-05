import datetime
class Package:
    def __init__(self, ID, address, city, state, zipcode, time_to_deliver, weight, status, truck):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.time_to_deliver = time_to_deliver
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = truck

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, Truck no.%s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.time_to_deliver, self.weight, self.delivery_time,
                                                       self.status, self.truck)
    #Method to update current status using comparison
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"