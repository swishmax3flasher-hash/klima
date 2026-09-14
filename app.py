import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Temperaturer Kirkenes Lufthavn, 2021-26",
    layout="centered",
)

st.title("Temperatur-svingninger basert på data fra seklima.met.no")
st.caption("En enkel Streamlit-innpakning for et script som lager én eller flere figurer fra faste data.")

# ------------------------------------------------------------
# 1) LIM INN / IMPORTER DIN EKSISTERENDE KODE HER
# ------------------------------------------------------------
# To vanlige mønstre:
# A) Du har koden i denne fila: legg den i funksjonen under.
# B) Du har koden i en annen fil, f.eks. analysis.py:
#    from analysis import make_figure
#    fig = make_figure()


def make_figure():
    plt.close('all')  # Tømmer minnet for plot
    """
    Temperaturplott for Kirkenes lufthavn, 2021-2026
    ****************************************************************
    Med utgangspunkt i dataene fra https://seklima.met.no/observations
    for de siste 5 åra, fordelt på måender, leger scriptet en minste
    kvadraters tilpasning til en sykslisk funskjon

    T(t) = A sin(2pi x) + B cos(2pi x) + C,

    basert på oppskrift og oppgave fra Eivind Schneiders 'Klimamatematikk 1.0'
    fra UiT, Norges Arktiske Universitet, kapitttel 2.

    Løsningsforslag for oppgave 2.9c, side 35

    Plottet viser et scatter-plott av temperaturmålingene, plotter den grafen som oppstår,
    viser gjennomsnittstemperatur og en lineær trendlinje for temperatur-utviklinga i perioden.
    
    Trendlinja må naturligvis tas med en stor klype salt, fordi perioden vi ser på er så
    kort, og fordi man lett kan vise at tilbake-rulling av dataene med simulerte temperaturer
    et par tiår tilbake, vil gi anslag for temperaturer som rett og slett er tåpelige.

    -------------------------------------------------------------------------------------------

    Det er nå mulig å laste inn data fra andre steder enn Kirkenes, ved at du henter dem ut
    fra https://seklima.met.no/observations og velger sted, og laster ned csv filer selv, som
    du kan mate inn her. 

    Men det er viktig at du kurerer csv filen før opplasting. Min erfaring er at det er en
    god del mangler ved disse filene, slik at temperatur-data, som skal være i kolonne 2,
    til høyre, mangler. Pass på at det er temperatur-data for alle måneder i denne kolonnen.

    Du må også slette første og siste kolonne fra csv-fila som skal lastes opp.

    Min erfaring er at xlsx filene fra seklima er bedre, og at kanskje den beste metoden
    foreløpig er å laste ned xlsx fila og så slette første og siste rad, før du lagrer 
    som csv og laster opp. 

    Jeg vet ikke hvor mye tid jeg får til å jobbe med denne appen framover, men håper at 
    noen kan se nytten i den.

    """

    # Definer liste for x (5 år med månedlige data = 60 måneder)
    # Tiden t måles i år, så vi deler på 12.0 for å få  / måneder av år
    t = np.arange(0, 60) / 12.0

   # ------------------------------------------------------------
    # 1) DATAINN: CSV-opplasting (siste kolonne = 60 temperaturverdier)
    # ------------------------------------------------------------
    # Forventning: CSV-filen har 60 rader, og SISTE kolonne inneholder månedlige middeltemperaturer.
    # Vi leser denne siste kolonnen med pandas og gjør den om til en numpy-array T.
    
    
    
    uploaded = st.file_uploader(
        "Last opp CSV (60 rader; siste kolonne = månedlig middeltemperatur)",
        type=["csv"],
    )
    
    T = None
    
    def _load_T_from_csv(file) -> np.ndarray:
        df = pd.read_csv(file)
        if df.shape[1] < 1:
            raise ValueError("CSV har ingen kolonner.")
    
        # Plukk siste kolonne og gjør om til numerisk
        s = pd.to_numeric(df.iloc[:, -1], errors="coerce")
        s = s.dropna()
    
        if len(s) != 60:
            raise ValueError(f"Forventet 60 tall i siste kolonne, men fant {len(s)}.")
    
        return s.to_numpy(dtype=float)
    
    try:
        if uploaded is not None:
            T = _load_T_from_csv(uploaded)
            st.success("CSV lastet. Fant 60 temperaturverdier i siste kolonne.")
        else:
            st.info("Ingen CSV lastet opp ennå. Bruker eksempeldata.")
            T = np.array([1.7, -6.1, -8.9, -8.6, -8.5, -3.2, -0.7, 4.1, 11.3, 15.1, 14.1, 7,
                          2.7, -2.4, -8.9, -5.9, -6.6, -8.7, 0.6, 7.5, 9.9, 12.2, 14.5, 9.2,
                          -0.3, -6.7, -10.8, -10.8, -9, -4.2, -2.8, 4.3, 9.8, 15.9, 15.9, 10.9,
                          2.8, -1.5, -7, -9.5, -3.6, -4.4, -2.6, 5.1, 9.1, 13.9, 13.1, 11,
                          3.7, -5.3, -6.5, -15.9, -12.5, -1.8, 1.8, 5.9, 11.4, 14.4, 11.8, 8.7], dtype=float)
    except Exception as e:
        st.error(str(e))
        st.stop()

    # Finn funksjonsverdiene for punktene
    # For å bruke funksjonene og pi kan man bruke numpy eller math
    fx = np.sin(2 * np.pi * t)
    gx = np.cos(2 * np.pi * t)
    hx = np.ones(len(t))  # Lager en liste/array med 1-tall, like lang som den for dataene

    # Regner ut summene (S-variablene)
    # Bruker her skrivemåten fra koden side 32 i Klima-heftet
    # Vi får tre summer, siden vi bruker 2 funksjoner + 1-erne
    S11 = sum([fx[i] * fx[i] for i in range(len(t))])  # sin*sin ledd
    S22 = sum([gx[i] * gx[i] for i in range(len(t))])  # cos*cos ledd
    S33 = sum([hx[i] * hx[i] for i in range(len(t))])  # 1*1 ledd

    # Kryssprodukter
    S12 = sum([fx[i] * gx[i] for i in range(len(t))])  # cos*sin ledd
    S13 = sum([fx[i] * hx[i] for i in range(len(t))])  # sin*1 ledd
    S23 = sum([gx[i] * hx[i] for i in range(len(t))])  # cos*1 ledd

    # Regner ut summene (R-variablene)
    R1 = sum([T[i] * fx[i] for i in range(len(t))])  # y-punkter ganger sin
    R2 = sum([T[i] * gx[i] for i in range(len(t))])  # y-punkter ganger cos
    R3 = sum([T[i] * hx[i] for i in range(len(t))])  # y-punkter ganger 1

    # Løser 3x3 likningssettet analytisk (Cramers regel)
    # Slik det gjøres på side 32 for et 2x2-system. Vi dropper S_matrise og np.linalg.solve,
    # og regner ut eksplisitt fra S- og R-variablene slik boka gjør for A og B.

    # Determinanten til  [hovedmatrisen], som blir nevneren for alle brøkene:
    D = S11 * (S22 * S33 - S23 * S23) - S12 * (S12 * S33 - S13 * S23) + S13 * (S12 * S23 - S13 * S22)

    # Finner A, B og C ved å regne ut tellerne via Cramers regel og dele på D:
    # De første delene av utregningene, før dette deles på D, er
    # determinantene til en modifisert hovedmatrise, der kolonne (søyle) 1, 2 og 3
    # byttes ut med de kjente verdiene (y) som representerer høyre side for hvert
    # likningssett
    A = (R1 * (S22 * S33 - S23 * S23) - S12 * (R2 * S33 - R3 * S23) + S13 * (R2 * S23 - R3 * S22)) / D
    B = (S11 * (R2 * S33 - R3 * S23) - R1 * (S12 * S33 - S13 * S23) + S13 * (S12 * R3 - S13 * R2)) / D
    C = (S11 * (S22 * R3 - S23 * R2) - S12 * (S12 * R3 - S13 * R2) + R1 * (S12 * S23 - S13 * S22)) / D

    print(f"Beste tilpasning: y = {A:.3f}*sin(2*pi*t) + {B:.3f}*cos(2*pi*t) + {C:.3f}")

    print(f"\nModellens gjennomsnittstemperatur (C) er {C:.1f}°C")

    # Plott datapunktene og den estimerte funksjonen
    # Lager ekstra mange punkter for at kurven skal se glatt og pen ut i plottet
    def Temp_glatt(t):
        return A * np.sin(2 * np.pi * t) + B * np.cos(2 * np.pi * t) + C

    t_glatt = np.linspace(0, 5, 200)

    T_glatt = Temp_glatt(t_glatt)

    plt.figure(num='Temperaturer', figsize=(12, 6))
    # Endre ikon
    # Plott de faktiske månedlige dataene som punkter
    plt.plot(t, T, 'go', label='Gjennomsnittlig månedstemperatur')
    # Plott den beregnede sinus-kurven
    plt.plot(t_glatt, T_glatt, color='orange', linewidth=2,
             label=fr'Modell: $T(t) = {A:.1f}\sin(2\pi t) {B:+.1f}\cos(2\pi t) {C:+.1f}$')

    # Gjennomsnitts-temperatur merkes med en striplet linje
    plt.axhline(y=C, color='green', linestyle='--', label='Gjennomsnitt: ' + str(round(C, 1)) + "°C")

    # Finner ei trendlinje for dataene - går temperaturene opp eller ned over tidsspennet?
    #  y = ax + b
    # '1' betyr at vi vil ha et polynom av 1. grad (en rett linje)
    a, b = np.polyfit(t, T, 1)
    trend = a * t + b
    if b < 0:  # Forhindrer at merkelappen skriver +- foran b
        plt.plot(t, trend, label=f'Trendlinje y={a:.2f}t{b:.2f}', color='violet', linewidth=2, linestyle='--')
    else:
        plt.plot(t, trend, label=f'Trendlinje y={a:.2f}t+{b:.2f}', color='violet', linewidth=2, linestyle='--')

    # Dine posisjoner for GRID-linjene (strekene)
    grid_posisjoner = [0.25, 1.25, 2.25, 3.25, 4.25]

    # Posisjoner for TEKSTEN (midt mellom grid-linjene)
    tekst_posisjoner = [0.75, 1.75, 2.75, 3.75, 4.75]
    aarstall = [2022, 2023, 2024, 2025, 2026]

    ax = plt.gca()  # Henter den aktive grafen

    # 1. Plasser teksten på hovedmerkene (major ticks)
    plt.xticks(tekst_posisjoner, aarstall)

    # 2. Plasser de usynlige undermerkene der grid-linjene skal være (minor ticks)
    ax.set_xticks(grid_posisjoner, minor=True)

    # 3. Slå AV griden for teksten (major), og PÅ for de forskjøvne strekene (minor)
    ax.xaxis.grid(False, which='major')
    ax.xaxis.grid(True, which='minor', color='gray', linestyle='-')  # Velg farge/stil her

    # Tekster
    plt.xlabel('Tid (år)')
    plt.ylabel('Temperatur (°C)')
    plt.title(
        'Minste kvadraters metode for temperatur (Oppgave 2.9 c)')
    plt.legend(loc='lower left')  # Plasserer boksen med forklaring

    # Vil merke av hvilke måneder punktene tilhører
    # Liste med forbokstavene til månedene
    maaneder = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    # Går gjennom alle punktene for å sette på bokstaver
    for i in range(len(T)):
        # i % 12 (modulo) gjør at indeksen starter på 0 igjen hver gang vi passerer 12.
        # Dermed gjentas J, F, M... for hvert nytt år. Starter på oktober, så trekk fra 9 på i
        mnd_bokstav = maaneder[(i + 9) % 12]  # Modulus, heltallsdivisjon

        # Finner x- og y-koordinaten til akkurat dette punktet.
        # Husk å legge til f.eks. 2000 her også, hvis du gjorde det i plt.scatter!
        x_pos = t[i]
        y_pos = T[i]

        # Setter inn bokstaven.
        # xytext=(0, 7) og "offset points" flytter bokstaven 7 piksler rett opp fra prikken,
        # slik at de ikke overlapper og blir uleselige.
        plt.annotate(mnd_bokstav, (x_pos, y_pos), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8)

    # plt.savefig("opp_2_9_Kirkenes.jpg")  # Lagrer plottet som bilde

    # plt.show()  # Viser plottet
    fig = plt.gcf()
    return fig


# ------------------------------------------------------------
# 2) KJØR OG VIS RESULTATET
# ------------------------------------------------------------
with st.spinner("Genererer figur …"):
    fig = make_figure()

with st.container(border=True):
    st.subheader("Plott")
    st.pyplot(fig, clear_figure=False)


st.divider()

with st.expander("Kode til oprinnelige python fil (PyCharm 2025.3.2.1, python 3.14)"):
    st.markdown(
        """
1. Legg `app.py` i et GitHub-repo.
2. Lag en `requirements.txt` i samme repo med f.eks.:
   - `streamlit`
   - `numpy`
   - `matplotlib`
3. Gå til Streamlit Community Cloud og velg **Deploy** fra repoet.

Tips: Hvis du har flere figurer, kan du returnere en liste av `fig`-objekter og vise dem med flere `st.pyplot(...)`.
        """
    )
