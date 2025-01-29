import json
from math import *

print("\n")
ACTULOAD = open("ACTU.json", "r").read()
DECILOAD = open("DECISION.json", "r").read()
FUTURLOAD = open("FUTUR.json", "w")
RESULT = open("RESULT.txt", "w")

ACTU = json.loads(ACTULOAD)
DECI = json.loads(DECILOAD)

SALAIRE_OUVRIER = 7.5
EMBAUCHE_OUVRIER = 0.75
SALAIRE_VENDEUR = 12.5
ENCADREMENT_VENDEUR = 375
DEPLACEMENT_VENDEUR = 10
EMBAUCHE_VENDEUR = 5
ADMINISTRATION = 3000
MAITRISE_FIXE = 1750
MAX_PROD_MX = 35000
MAX_PROD_MY = 25000
VAR_MAX = 22



COUT_MAIN_DOEUVRE = (
    ceil(
        SALAIRE_OUVRIER * (ACTU["OUVRIERS"] + DECI["NEW_OUVRIERS"])
        + EMBAUCHE_OUVRIER * DECI["NEW_OUVRIERS"]
    )
    + MAITRISE_FIXE
)
COUT_COMMERCIAUX = ceil(
    SALAIRE_VENDEUR * (ACTU["VENDEURS"] + DECI["NEW_VENDEURS"])
    + DEPLACEMENT_VENDEUR * (ACTU["VENDEURS"] + DECI["NEW_VENDEURS"])
    + EMBAUCHE_VENDEUR * DECI["NEW_VENDEURS"]
    + ENCADREMENT_VENDEUR
    + DECI["PUB"]["Elite"]
    + DECI["PUB"]["2000"]
    + DECI["PUB"]["Raquette"]
)


DECI_PROD_TOT = DECI["PROD"]["Elite"] + DECI["PROD"]["2000"] + DECI["PROD"]["Raquette"]
DECI_PROD_TOT_PREV = (
    DECI["PROD"]["Elite"] * DECI["PREV_VOLUME_VENTE"]["Elite"]
    + DECI["PROD"]["2000"] * DECI["PREV_VOLUME_VENTE"]["2000"]
    + DECI["PROD"]["Raquette"] * DECI["PREV_VOLUME_VENTE"]["Raquette"]
) / 100

PROD_OUVRIERS = (ACTU["OUVRIERS"] + DECI["NEW_OUVRIERS"]) * 200

AMORTISSEMENT_MX = sum(
    [
        (125 * (ACTU["AGE_MX"][i] + ACTU["T"] + 1) if i < len(ACTU["AGE_MX"]) else 100)
        for i in range(len(ACTU["AGE_MX"]) + DECI["NEW_MX"])
    ]
)
AMORTISSEMENT_MY_FUTUR = sum(
    [
        (100 * (ACTU["AGE_MY"][i] + ACTU["T"] + 1) if i < len(ACTU["AGE_MY"]) else 100)
        for i in range(len(ACTU["AGE_MY"]) + DECI["NEW_MY"])
    ]
)
CHARGE_AMORTISSEMENT_MX = 125 * (len(ACTU["AGE_MX"]) + DECI["NEW_MX"])
CHARGE_AMORTISSEMENT_MY = 100 * (len(ACTU["AGE_MY"]) + DECI["NEW_MY"])
CHARGE_AMORTISSEMENT = CHARGE_AMORTISSEMENT_MX + CHARGE_AMORTISSEMENT_MY

COUTS_VAR_MAX = (
    VAR_MAX * (DECI["PROD"]["Elite"] + DECI["PROD"]["2000"] + DECI["PROD"]["Raquette"])
)

VAR_STOCKS_PREV = ceil(
    (
        (
            (ACTU["STOCKSPF"]["Elite"]/1000 + DECI["PROD"]["Elite"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["Elite"])
            / 100
            - ACTU["STOCKSPF"]["Elite"]/1000
        )
        * DECI["PRIX"]["Elite"]
        + (
            (ACTU["STOCKSPF"]["2000"]/1000 + DECI["PROD"]["2000"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["2000"])
            / 100
            - ACTU["STOCKSPF"]["2000"]/1000
        )
        * DECI["PRIX"]["2000"]
        + (
            (ACTU["STOCKSPF"]["Raquette"]/1000 + DECI["PROD"]["Raquette"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["Raquette"])
            / 100
            - ACTU["STOCKSPF"]["Raquette"]/1000
        )
        * DECI["PRIX"]["Raquette"]
    )
)
DECAISSEMENT = 0

CHARGES_ADMINISTRATIVES = ADMINISTRATION + DECI["QVT"] + 10*(DECI["ETUDE"]["SKI"]+DECI["ETUDE"]["Raquette"]) + DECI["ETUDE"]["ANALYTIQUE"]*250


def NB_MAT():
    ELITE = [DECI["PROD"]["Elite"] * 16, DECI["PROD"]["Elite"] * 4]
    SKI2000 = [
        DECI["PROD"]["2000"] * DECI["QUALITE"] / 5,
        DECI["PROD"]["2000"] * (100 - DECI["QUALITE"]) / 5,
    ]
    RAQUETTE = [DECI["PROD"]["Raquette"] * 5, DECI["PROD"]["Raquette"] * 5]
    RES = [
        ceil(ELITE[0] + SKI2000[0] + RAQUETTE[0]),
        ceil(ELITE[1] + SKI2000[1] + RAQUETTE[1]),
    ]
    return RES

def COUT_MAT_TEST(a, b):
    MAT =  NB_MAT()
    RES = ((MAT[0]+a)*(DECI["PRIX_MATERIAUX"][2]*DECI["RECYCLE"]["FIBRE"]/100 + DECI["PRIX_MATERIAUX"][0]*(100-DECI["RECYCLE"]["FIBRE"])/100) + (MAT[1]+b)*(DECI["PRIX_MATERIAUX"][3]*DECI["RECYCLE"]["RESINE"]/100 + DECI["PRIX_MATERIAUX"][1]*(100-DECI["RECYCLE"]["RESINE"])/100))
    return ceil(RES)

def COUT_MAT_ACTU():
    RES = 0
    RES += (
        ACTU["PRIX_MATERIAUX"][0] * (100 - ACTU["STOCKS_ACHETE"]["RECYCLE_FIBRE"]) / 100
        + ACTU["STOCKS_ACHETE"]["RECYCLE_FIBRE"] / 100 * ACTU["PRIX_MATERIAUX"][2]
    ) * ACTU["STOCKS_ACHETE"]["FIBRE"] + (
        ACTU["PRIX_MATERIAUX"][1] * (100 - ACTU["STOCKS_ACHETE"]["RECYCLE_RESINE"]) / 100
        + ACTU["STOCKS_ACHETE"]["RECYCLE_RESINE"] / 100 * ACTU["PRIX_MATERIAUX"][3]
    ) * ACTU[
        "STOCKS_ACHETE"
    ][
        "RESINE"
    ]

    RES = ceil(RES)
    return RES


def COUT_MAT_PREV():
    RES = 0
    RES += (
        (
            16
            * (
                DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
            )
            + 4
            * (
                DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
            )
        )
        * DECI["PROD"]["Elite"]
    )
    RES += (
        (
            DECI["QUALITE"]
            / 5
            * (
                DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
            )
            + (100 - DECI["QUALITE"])
            / 5
            * (
                DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
            )
        )
        * DECI["PROD"]["2000"]
    )
    RES += (
        (
            5
            * (
                DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
            )
            + 5
            * (
                DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
            )
        )
        * DECI["PROD"]["Raquette"]
    )
    RES = ceil(RES)
    return RES


def CALCUL_COUT_PROD_PREV():
    RES = (
        COUT_MAIN_DOEUVRE
        + COUTS_VAR_MAX
        + DECI["R&D"]
        + CHARGE_AMORTISSEMENT
        + DECI["PROD_ECO"]
        # + VAR_STOCKS_PREV
        + COUT_MAT_PREV()
    )
    return RES



def CALCUL_PRIX_UNITAIRE_PREV():
    COUT_PROD_PREV = CALCUL_COUT_PROD_PREV() - COUT_MAT_PREV()
    PRIX_ELITE = (
        DECI["PUB"]["Elite"]
        / (DECI["PROD"]["Elite"] * DECI["PREV_VOLUME_VENTE"]["Elite"] / 100)
        if DECI["PROD"]["Elite"] != 0
        else 0
    )
    PRIX_2000 = (
        DECI["PUB"]["2000"]
        / (DECI["PROD"]["2000"] * DECI["PREV_VOLUME_VENTE"]["2000"] / 100)
        if DECI["PROD"]["2000"] != 0
        else 0
    )
    PRIX_RAQUETTE = (
        DECI["PUB"]["Raquette"]
        / (DECI["PROD"]["Raquette"] * DECI["PREV_VOLUME_VENTE"]["Raquette"] / 100)
        if DECI["PROD"]["Raquette"] != 0
        else 0
    )
    PRIX_ELITE += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["Elite"] != 0 else 0
    PRIX_2000 += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["2000"] != 0 else 0
    PRIX_RAQUETTE += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["Raquette"] != 0 else 0
    PRIX_ELITE += 16 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + 4 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_2000 += DECI["QUALITE"] / 5 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + (100 - DECI["QUALITE"]) / 5 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_RAQUETTE += 5 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + 5 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_ELITE = "{:.2f}".format(PRIX_ELITE)
    PRIX_2000 = "{:.2f}".format(PRIX_2000)
    PRIX_RAQUETTE = "{:.2f}".format(PRIX_RAQUETTE)

    print(
        "PRIX ELITE,    PRIX 2000,    PRIX RAQUETTE \n",
        [PRIX_ELITE, PRIX_2000, PRIX_RAQUETTE],
        "\n",
    )
    return [PRIX_ELITE, PRIX_2000, PRIX_RAQUETTE]

def CALCUL_PRIX_UNITAIRE_PREV_V2():
    COUT_PROD_PREV = CALCUL_COUT_PROD_PREV() - COUT_MAT_PREV()
    PRIX_ELITE = (
        DECI["PUB"]["Elite"]
        / DECI["PROD"]["Elite"]
        if DECI["PROD"]["Elite"] != 0
        else 0
    )
    PRIX_2000 = (
        DECI["PUB"]["2000"]
        / DECI["PROD"]["2000"]
        if DECI["PROD"]["2000"] != 0
        else 0
    )
    PRIX_RAQUETTE = (
        DECI["PUB"]["Raquette"]
        / DECI["PROD"]["Raquette"]
        if DECI["PROD"]["Raquette"] != 0
        else 0
    )
    PRIX_ELITE += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["Elite"] != 0 else 0
    PRIX_2000 += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["2000"] != 0 else 0
    PRIX_RAQUETTE += COUT_PROD_PREV / DECI_PROD_TOT_PREV if DECI["PROD"]["Raquette"] != 0 else 0
    PRIX_ELITE += 16 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + 4 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_2000 += DECI["QUALITE"] / 5 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + (100 - DECI["QUALITE"]) / 5 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_RAQUETTE += 5 * (
        DECI["PRIX_MATERIAUX"][0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * DECI["PRIX_MATERIAUX"][2]
    ) + 5 * (
        DECI["PRIX_MATERIAUX"][1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * DECI["PRIX_MATERIAUX"][3]
    )
    PRIX_ELITE = "{:.2f}".format(PRIX_ELITE)
    PRIX_2000 = "{:.2f}".format(PRIX_2000)
    PRIX_RAQUETTE = "{:.2f}".format(PRIX_RAQUETTE)

    print(
        "PRIX ELITE,    PRIX 2000,    PRIX RAQUETTE \n",
        [PRIX_ELITE, PRIX_2000, PRIX_RAQUETTE],
        "\n",
    )
    return [PRIX_ELITE, PRIX_2000, PRIX_RAQUETTE]


def CALCUL_PROD_TOT_MX():
    MACHINES = 0
    for i in range(len(ACTU["AGE_MX"]) + DECI["NEW_MX"]):
        MACHINES += (
            MAX_PROD_MX - (1750 * (ACTU["AGE_MX"][i] + ACTU["T"]))
            if i < len(ACTU["AGE_MX"])
            else MAX_PROD_MX
        )
    MACHINES_SURCHARGE = 1.5 * MACHINES
    print("MX SANS SURCHARGE : ", MACHINES)
    print("MX AVEC SURCHARGE : ", MACHINES_SURCHARGE, "\n")
    return [MACHINES, MACHINES_SURCHARGE]


def CALCUL_PROD_TOT_MY():
    MACHINES = 0
    for i in range(len(ACTU["AGE_MY"]) + DECI["NEW_MY"]):
        MACHINES += (
            MAX_PROD_MY - (1250 * (ACTU["AGE_MY"][i] + ACTU["T"]))
            if i < len(ACTU["AGE_MY"])
            else MAX_PROD_MY
        )
    MACHINES_SURCHARGE = 1.5 * MACHINES
    print("MY SANS SURCHARGE : ", MACHINES)
    print("MY AVEC SURCHARGE : ", MACHINES_SURCHARGE, "\n")
    return [MACHINES, MACHINES_SURCHARGE]


def CA_PREV():
    RES = 0
    RES += (
        DECI["PRIX"]["Elite"]
        * DECI["PREV_VOLUME_VENTE"]["Elite"]
        / 100
        * (DECI["PROD"]["Elite"] + ACTU["STOCKSPF"]["Elite"]/1000)
        + DECI["PRIX"]["2000"]
        * (DECI["PROD"]["2000"] + ACTU["STOCKSPF"]["2000"]/1000)
        * DECI["PREV_VOLUME_VENTE"]["2000"]
        / 100
        + DECI["PRIX"]["Raquette"]
        * (DECI["PROD"]["Raquette"] + ACTU["STOCKSPF"]["Raquette"]/1000)
        * DECI["PREV_VOLUME_VENTE"]["Raquette"]
        / 100
    )
    return ceil(RES)


def CA_EXACT():
    RES = (
        ACTU["PRIX"]["Elite"] * ACTU["VENTES"]["Elite"]
        + ACTU["PRIX"]["2000"] * ACTU["VENTES"]["2000"]
        + ACTU["PRIX"]["Raquette"] * ACTU["VENTES"]["Raquette"]
    )
    return ceil((RES) / 1000)


DECAISSEMENT = (
    COUT_MAT_ACTU()
    + 2500 * DECI["NEW_MX"]
    + 2000 * DECI["NEW_MY"]
    + COUT_MAIN_DOEUVRE
    + COUT_COMMERCIAUX
    + ADMINISTRATION
    + ACTU["EMPRUNT"]
)
ENCAISSEMENT = (
    (100 - ACTU["ESCOMPTE"]) / 100 * CA_EXACT()
    + DECI["ESCOMPTE"] / 100 * CA_PREV()
    + DECI["EMPRUNTS"]["CT"]
    + DECI["EMPRUNTS"]["LT"]
    + ACTU["TREZO"]
)
BENEF_PREV = ceil((CA_PREV() - CALCUL_COUT_PROD_PREV() - CHARGES_ADMINISTRATIVES)*(0.7 if (CA_PREV() - CALCUL_COUT_PROD_PREV()-CHARGES_ADMINISTRATIVES) > 0 else 1))
TREZO_FUTURE = ENCAISSEMENT - DECAISSEMENT
DECAISSEMENT += TREZO_FUTURE
ARGENT_DISPO_ACTU = ceil(ACTU["TREZO"]+(100 - ACTU["ESCOMPTE"]) / 100 * CA_EXACT())
COUTS_ACTUELS = CALCUL_COUT_PROD_PREV() + COUT_COMMERCIAUX + CHARGES_ADMINISTRATIVES + COUT_MAT_ACTU() + 2500 * DECI["NEW_MX"] + 2000 * DECI["NEW_MY"] - COUT_MAT_PREV() + ACTU["EMPRUNT"] + DECI["DIVIDENDE"]


print("Couts ouvriers : ", COUT_MAIN_DOEUVRE)
print("COUT_COMMERCIAUX : ", COUT_COMMERCIAUX)
print("\n")
mx = CALCUL_PROD_TOT_MX()
my = CALCUL_PROD_TOT_MY()
print("Prod Ouvriers : ", PROD_OUVRIERS)
print("Prod totale demadées", DECI_PROD_TOT * 1000)
print("Nombre Prod MAXX : ", mx[1] + my[1])
print("Nombre Ouvrier MAXX : ", ceil((mx[1] + my[1]) / 200))
print(
    "Nombre NEW Ouvrier MAXX : ", ceil((mx[1] + my[1]) / 200) - ACTU["OUVRIERS"], "\n"
)
CALCUL_PRIX_UNITAIRE_PREV()
CALCUL_PRIX_UNITAIRE_PREV_V2()

print("Nombre Matériaux : ", NB_MAT(), "\n")

print("CA Prévisionnel : ", ceil(CA_PREV()))
print("CA Exact Période Passée: ", CA_EXACT(), "\n")

print("Amortissement MX : ", AMORTISSEMENT_MX)
print("Amortissement MY : ", AMORTISSEMENT_MY_FUTUR)
print("Charge Amortissement MX : ", CHARGE_AMORTISSEMENT_MX)
print("Charge Amortissement MY : ", CHARGE_AMORTISSEMENT_MY)
print("Charge Amortissement : ", CHARGE_AMORTISSEMENT_MX + CHARGE_AMORTISSEMENT_MY, "\n")

print("Couts PRODUCTION Prévisionnel : ", CALCUL_COUT_PROD_PREV(), "\n")

print("Couts MATERIAUX Prévisionnel : ", COUT_MAT_PREV(), " VERIF : ", COUT_MAT_TEST(-1100, -1675))
print("Couts MATERIAUX Actuel : ", COUT_MAT_ACTU(), "\n")

print("Décaissement : ", ceil(DECAISSEMENT))
print("Encaissement : ", ceil(ENCAISSEMENT), "\n")

print("Tresorerie Actuelle : ", ACTU["TREZO"])
print("Trésorerie Future : ", ceil(TREZO_FUTURE), "\n")

print("Argent Dispo : ", ARGENT_DISPO_ACTU)
print("Couts ACTUELS : ", COUTS_ACTUELS)
print("Couts Argent Dispo (escompte) : ", ARGENT_DISPO_ACTU, "\n")

print("Bénéfice Possible : ", BENEF_PREV)
