from django.db import models

# Create your models here.
class State(models.Model):
    state_fips = models.CharField(max_length=2, primary_key=True)
    state_code = models.CharField(max_length=2, unique=True)
    state_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.state_fips} - {self.state_code} - {self.state_name}"

class County(models.Model):
    county_fips = models.CharField(max_length=5, primary_key=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    county_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.county_fips} - {self.state.state_code} - {self.county_name}"

    class Meta:
        unique_together = ("state", "county_name")

class Candidate(models.Model):
    candidate_name = models.CharField(max_length=128)

    def __str__(self):
        return self.candidate_name

class Party(models.Model):
    party = models.CharField(max_length=128, unique=True, null=False, blank=False)
    color_hex = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.party

class StateResults(models.Model):
    year = models.SmallIntegerField(null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)
    candidate_votes = models.IntegerField(null=False, blank=False)
    total_votes = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.year} - {self.state.state_code} - {self.party.party_code} - {self.candidate.candidate_name} - {self.candidate_votes} - {self.total_votes}"

    class Meta:
        unique_together = ("year", "state", "candidate")

class CountyResults(models.Model):
    year = models.SmallIntegerField(null=False, blank=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)
    candidate_votes = models.IntegerField(null=False, blank=False)
    total_votes = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.year} - {self.county.state.state_code} - {self.county.county_name} - {self.party.party_code} - {self.candidate.candidate_name} - {self.candidate_votes} - {self.total_votes}"

    class Meta:
        unique_together = ("year", "county", "candidate")