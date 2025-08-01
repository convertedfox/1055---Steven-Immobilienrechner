import streamlit as st

st.set_page_config(page_title="Immobilien-Leistbarkeitsrechner", layout="centered")

st.title("🏡 Immobilien-Leistbarkeitsrechner für Steven ♥️")

st.markdown("""
Mit diesem Tool kannst du berechnen, ob du Dir einen Immobilienkredit für eine bestimmte Immobilie leisten kannst – im Vergleich zu deinem Einkommen und deiner aktuellen Miete.
""")

st.header("🔢 Eingabedaten")

kaufpreis = st.number_input("Kaufpreis der Immobilie (€)", value=400_000, step=10_000)
eigenkapital = st.number_input("Eigenkapital (€)", value=70_000, step=5_000)
zinssatz = st.number_input("Effektiver Jahreszins (%)", value=4.0, step=0.1)
tilgung = st.number_input("Anfängliche Tilgung (%)", value=2.0, step=0.1)
gehalt = st.number_input("Monatliches Nettoeinkommen (€)", value=4_000, step=100)
miete = st.number_input("Deine derzeitige Miete (€)", value=1_200, step=50)

# Berechnungen
darlehensbetrag = kaufpreis - eigenkapital
annuitaet = darlehensbetrag * (zinssatz + tilgung) / 100 / 12
belastungsquote = annuitaet / gehalt * 100
differenz_zur_miete = annuitaet - miete

st.header("📊 Ergebnis")

st.write(f"**Benötigter Kreditbetrag:** {darlehensbetrag:,.0f} €")
st.write(f"**Monatliche Rate (Annuität):** {annuitaet:,.2f} €")
st.write(f"**Belastungsquote:** {belastungsquote:.1f} % deines Nettoeinkommens")
st.write(f"**Vergleich zur Miete:** {'Mehr' if differenz_zur_miete > 0 else 'Weniger'} als derzeitige Miete: {abs(differenz_zur_miete):,.2f} €")

# Bewertung
st.subheader("💡 Einschätzung")
if belastungsquote < 30:
    st.success("Sehr gut! Die Rate liegt deutlich unter 30 % deines Einkommens.")
elif belastungsquote < 40:
    st.info("Akzeptabel. Die Belastung ist noch im empfohlenen Rahmen (max. 40 %).")
else:
    st.warning("Vorsicht! Die Rate übersteigt 40 % deines Einkommens. Das ist riskant.")

