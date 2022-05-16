class OrganisationType:
    FOUNDATION = 0
    NON_GOV_ORGANIZATION = 1
    FUND_RAISER = 2

    CHOICES = (
        (FOUNDATION, 'Fundacja'),
        (NON_GOV_ORGANIZATION, 'Organizacja pozarządowa'),
        (FUND_RAISER, 'Zbiórka lokalna'),
    )