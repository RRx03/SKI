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
PRIX_MATERIAUX = [5.5, 1.75, 6.6, 2.28]


COUT_MAIN_DOEUVRE = (
    ceil(
        SALAIRE_OUVRIER * (ACTU["OUVRIERS"] + DECI["NEW_OUVRIERS"])
        + EMBAUCHE_OUVRIER * DECI["NEW_OUVRIERS"]
    )
    + 1750
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
    25 * (DECI["PROD"]["Elite"] + DECI["PROD"]["2000"] + DECI["PROD"]["Raquette"])
) / 1000

VAR_STOCKS_PREV = ceil(
    (
        (
            (ACTU["STOCKSPF"]["Elite"] + DECI["PROD"]["Elite"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["Elite"])
            / 100
            - ACTU["STOCKSPF"]["Elite"]
        )
        * DECI["PRIX"]["Elite"]
        + (
            (ACTU["STOCKSPF"]["2000"] + DECI["PROD"]["2000"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["2000"])
            / 100
            - ACTU["STOCKSPF"]["2000"]
        )
        * DECI["PRIX"]["2000"]
        + (
            (ACTU["STOCKSPF"]["Raquette"] + DECI["PROD"]["Raquette"])
            * (100 - DECI["PREV_VOLUME_VENTE"]["Raquette"])
            / 100
            - ACTU["STOCKSPF"]["Raquette"]
        )
        * DECI["PRIX"]["Raquette"]
    )
    / 1000
)

DECAISSEMENT = 0


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


def COUT_MAT_ACTU():
    RES = 0
    RES += (
        PRIX_MATERIAUX[0] * (100 - ACTU["STOCKS_ACHETE"]["RECYCLE_FIBRE"]) / 100
        + ACTU["STOCKS_ACHETE"]["RECYCLE_FIBRE"] / 100 * PRIX_MATERIAUX[2]
    )*ACTU["STOCKS_ACHETE"]["FIBRE"] + (
        PRIX_MATERIAUX[1] * (100 - ACTU["STOCKS_ACHETE"]["RECYCLE_RESINE"]) / 100
        + ACTU["STOCKS_ACHETE"]["RECYCLE_RESINE"] / 100 * PRIX_MATERIAUX[3]
    )*ACTU["STOCKS_ACHETE"]["RESINE"]

    RES = ceil(RES)
    return RES


def COUT_MAT_PREV():
    RES = 0
    RES += (
        (
            16
            * (
                PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
            )
            + 4
            * (
                PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
            )
        )
        * DECI["PROD"]["Elite"]
        * DECI["PREV_VOLUME_VENTE"]["Elite"]
        / 100
    )
    RES += (
        (
            DECI["QUALITE"]
            / 5
            * (
                PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
            )
            + (100 - DECI["QUALITE"])
            / 5
            * (
                PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
            )
        )
        * DECI["PROD"]["2000"]
        * DECI["PREV_VOLUME_VENTE"]["2000"]
        / 100
    )
    RES += (
        (
            5
            * (
                PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
                + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
            )
            + 5
            * (
                PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
                + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
            )
        )
        * DECI["PROD"]["Raquette"]
        * DECI["PREV_VOLUME_VENTE"]["Raquette"]
        / 100
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
        + VAR_STOCKS_PREV
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
    PRIX_ELITE += COUT_PROD_PREV / DECI_PROD_TOT_PREV
    PRIX_2000 += COUT_PROD_PREV / DECI_PROD_TOT_PREV
    PRIX_RAQUETTE += COUT_PROD_PREV / DECI_PROD_TOT_PREV
    PRIX_ELITE += 16 * (
        PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
    ) + 4 * (
        PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
    )
    PRIX_2000 += DECI["QUALITE"] / 5 * (
        PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
    ) + (100 - DECI["QUALITE"]) / 5 * (
        PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
    )
    PRIX_RAQUETTE += 5 * (
        PRIX_MATERIAUX[0] * (100 - DECI["RECYCLE"]["FIBRE"]) / 100
        + DECI["RECYCLE"]["FIBRE"] / 100 * PRIX_MATERIAUX[2]
    ) + 5 * (
        PRIX_MATERIAUX[1] * (100 - DECI["RECYCLE"]["RESINE"]) / 100
        + DECI["RECYCLE"]["RESINE"] / 100 * PRIX_MATERIAUX[3]
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
        * (DECI["PROD"]["Elite"] + ACTU["STOCKSPF"]["Elite"])
        + DECI["PRIX"]["2000"]
        * (DECI["PROD"]["2000"] + ACTU["STOCKSPF"]["2000"])
        * DECI["PREV_VOLUME_VENTE"]["2000"]
        / 100
        + DECI["PRIX"]["Raquette"]
        * (DECI["PROD"]["Raquette"] + ACTU["STOCKSPF"]["2000"])
        * DECI["PREV_VOLUME_VENTE"]["Raquette"]
        / 100
    )
    print("CA Prévisionnel : ", ceil(RES))
    return ceil(RES)


def CA_EXACT():
    print(
        "CA Exact Période Passée: ",
        ceil(
            (
                ACTU["PRIX"]["Elite"] * ACTU["VENTES"]["Elite"]
                + ACTU["PRIX"]["2000"] * ACTU["VENTES"]["2000"]
                + ACTU["PRIX"]["Raquette"] * ACTU["VENTES"]["Raquette"]
            )
            / 1000
        ),
        "\n",
    )

DECAISSEMENT = COUT_MAT_ACTU() + 2500*DECI["NEW_MX"] + 2000*DECI["NEW_MY"] + COUT_MAIN_DOEUVRE + COUT_COMMERCIAUX + ADMINISTRATION #(+IMPOTS+emprunts etc)

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

print("Nombre Matériaux : ", NB_MAT(), "\n")

CA_PREV()
CA_EXACT()
print("Amortissement MX : ", AMORTISSEMENT_MX)
print("Amortissement MY : ", AMORTISSEMENT_MY_FUTUR)
print("Charge Amortissement MX : ", CHARGE_AMORTISSEMENT_MX)
print("Charge Amortissement MY : ", CHARGE_AMORTISSEMENT_MY)
print("Charge Amortissement : ", CHARGE_AMORTISSEMENT_MX + CHARGE_AMORTISSEMENT_MY)

print("Couts Production Prévisionnel : ", CALCUL_COUT_PROD_PREV())
print("Couts Matériaux Prévisionnel : ", COUT_MAT_PREV())
print("Couts Matériaux Actuel : ", COUT_MAT_ACTU())
print("Décaissement : ", DECAISSEMENT)
