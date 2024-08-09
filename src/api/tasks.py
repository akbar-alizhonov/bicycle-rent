from celery import shared_task

from bicycle.models import Rental, Bicycle


@shared_task
def calculate_rental_cost(rental_id):
    rental = Rental(id=rental_id)
    bicycle = rental.bicycle
    bicycle.status = Bicycle.BicycleStatus.available
    duration = rental.end_time - rental.start_time
    rental.cost = (duration.total_seconds() / 3600) * int(bicycle.price)

    bicycle.save()
    rental.save()