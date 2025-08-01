import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Immobilien-Leistbarkeitsrechner", layout="centered")

st.title("🏡 Immobilien-Leistbarkeitsrechner für Steven ♥️")

st.markdown("""
Mit diesem Tool kannst du berechnen, ob du dir einen Immobilienkredit für eine bestimmte Immobilie leisten kannst – 
im Vergleich zu deinem Einkommen und deiner aktuellen Miete.
""")

# Sidebar für erweiterte Optionen
with st.sidebar:
    st.header("⚙️ Erweiterte Einstellungen")
    laufzeit = st.slider("Kreditlaufzeit (Jahre)", min_value=10, max_value=40, value=30)
    nebenkosten_prozent = st.slider("Nebenkosten (%)", min_value=5.0, max_value=15.0, value=10.0, step=0.5)
    lebenshaltungskosten = st.number_input("Monatliche Lebenshaltungskosten (€)", value=2000, step=100)

st.header("🔢 Eingabedaten")

col1, col2 = st.columns(2)

with col1:
    st.write("**Kaufpreis der Immobilie:**")
    st.caption("Der Preis, den du für die Immobilie zahlen möchtest.")
    kaufpreis = st.number_input("Kaufpreis der Immobilie (€)", value=400_000, step=10_000)
    
    st.write("**Eigenkapital:**")
    st.caption("Das Geld, das du selbst einbringst. Mindestens 20% empfohlen!")
    eigenkapital = st.number_input("Eigenkapital (€)", value=70_000, step=5_000)
    
    st.write("**Effektiver Jahreszins:**")
    st.caption("Der Zinssatz, den die Bank für den Kredit verlangt.")
    zinssatz = st.number_input("Effektiver Jahreszins (%)", value=4.0, step=0.1)

with col2:
    st.write("**Anfängliche Tilgung:**")
    st.caption("Höhere Tilgung = schnellere Rückzahlung!")
    tilgung = st.number_input("Anfängliche Tilgung (%)", value=2.0, step=0.1)
    
    st.write("**Monatliches Nettoeinkommen:**")
    gehalt = st.number_input("Monatliches Nettoeinkommen (€)", value=4_000, step=100)
    
    st.write("**Derzeitige Miete:**")
    st.caption("Zum Vergleich mit der Kreditrate")
    miete = st.number_input("Deine derzeitige Miete (€)", value=1_200, step=50)

# Berechnungen
nebenkosten = kaufpreis * nebenkosten_prozent / 100
gesamtkosten = kaufpreis + nebenkosten
darlehensbetrag = gesamtkosten - eigenkapital
eigenkapitalquote = eigenkapital / gesamtkosten * 100

# Monatliche Rate berechnen
monatszins = zinssatz / 100 / 12
gesamttilgung = zinssatz + tilgung
annuitaet = darlehensbetrag * gesamttilgung / 100 / 12

# Alternative Berechnung mit korrekter Annuitätsformel
if zinssatz > 0:
    q = 1 + monatszins
    n = laufzeit * 12
    annuitaet_korrekt = darlehensbetrag * (monatszins * q**n) / (q**n - 1)
else:
    annuitaet_korrekt = darlehensbetrag / (laufzeit * 12)

belastungsquote = annuitaet_korrekt / gehalt * 100
differenz_zur_miete = annuitaet_korrekt - miete
verfuegbares_einkommen = gehalt - annuitaet_korrekt - lebenshaltungskosten

st.header("📊 Ergebnis")

# Kennzahlen in Spalten
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Darlehensbetrag", f"{darlehensbetrag:,.0f} €")
with col2:
    st.metric("📅 Monatliche Rate", f"{annuitaet_korrekt:,.0f} €")
with col3:
    st.metric("📊 Belastungsquote", f"{belastungsquote:.1f}%")
with col4:
    st.metric("🏠 Eigenkapitalquote", f"{eigenkapitalquote:.1f}%")

# Detaillierte Aufschlüsselung
st.subheader("🔍 Detaillierte Aufschlüsselung")
col1, col2 = st.columns(2)

with col1:
    st.write("**Kostenaufstellung:**")
    st.write(f"• Kaufpreis: {kaufpreis:,.0f} €")
    st.write(f"• Nebenkosten ({nebenkosten_prozent}%): {nebenkosten:,.0f} €")
    st.write(f"• **Gesamtkosten: {gesamtkosten:,.0f} €**")
    st.write(f"• Eigenkapital: -{eigenkapital:,.0f} €")
    st.write(f"• **Darlehensbetrag: {darlehensbetrag:,.0f} €**")

with col2:
    st.write("**Monatliche Belastung:**")
    st.write(f"• Kreditrate: {annuitaet_korrekt:,.0f} €")
    st.write(f"• Derzeitige Miete: {miete:,.0f} €")
    differenz_text = "mehr" if differenz_zur_miete > 0 else "weniger"
    st.write(f"• **Differenz: {abs(differenz_zur_miete):,.0f} € {differenz_text}**")
    st.write(f"• Verfügbar nach Rate & Leben: {verfuegbares_einkommen:,.0f} €")

# Bewertung mit mehr Details
st.subheader("💡 Einschätzung")

# Ampel-System
if belastungsquote < 30 and eigenkapitalquote >= 20 and verfuegbares_einkommen > 500:
    st.success("✅ **Ausgezeichnet!** Die Finanzierung ist sehr solide.")
    bewertung = "Sehr gut"
elif belastungsquote < 40 and eigenkapitalquote >= 15 and verfuegbares_einkommen > 200:
    st.info("✅ **Gut.** Die Finanzierung ist machbar.")
    bewertung = "Gut"
elif belastungsquote < 45 and eigenkapitalquote >= 10:
    st.warning("⚠️ **Grenzwertig.** Prüfe deine Finanzen genau.")
    bewertung = "Grenzwertig"
else:
    st.error("❌ **Riskant!** Diese Finanzierung ist nicht empfehlenswert.")
    bewertung = "Riskant"

# Warnungen und Empfehlungen
if eigenkapitalquote < 20:
    st.warning(f"⚠️ **Niedriges Eigenkapital:** Mit {eigenkapitalquote:.1f}% liegt dein Eigenkapital unter den empfohlenen 20%. Dies kann zu höheren Zinsen führen.")

if verfuegbares_einkommen < 200:
    st.error(f"❌ **Zu wenig Puffer:** Nach Kreditrate und Lebenshaltungskosten bleiben nur {verfuegbares_einkommen:,.0f} € übrig. Das ist zu wenig für unvorhergesehene Ausgaben.")

# Visualisierung
st.subheader("📈 Visualisierung")

# Kreisdiagramm für Einkommensverteilung
fig_pie = go.Figure(data=[go.Pie(
    labels=['Kreditrate', 'Lebenshaltungskosten', 'Verfügbar'],
    values=[annuitaet_korrekt, lebenshaltungskosten, max(0, verfuegbares_einkommen)],
    hole=.3
)])
fig_pie.update_layout(title="Verteilung des monatlichen Nettoeinkommens")
st.plotly_chart(fig_pie, use_container_width=True)

# Vergleichsbalken
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(name='Kosten', x=['Kreditrate', 'Derzeitige Miete'], 
                        y=[annuitaet_korrekt, miete],
                        marker_color=['lightcoral', 'lightblue']))
fig_bar.update_layout(title="Vergleich: Kreditrate vs. derzeitige Miete", yaxis_title="Euro (€)")
st.plotly_chart(fig_bar, use_container_width=True)

# Tipps
st.subheader("💡 Tipps zur Optimierung")
if belastungsquote > 35:
    st.write("• Erhöhe dein Eigenkapital um die monatliche Belastung zu senken")
    st.write("• Verlängere die Laufzeit für niedrigere Monatsraten")
    st.write("• Suche nach Immobilien in niedrigeren Preisklassen")

if eigenkapitalquote < 20:
    st.write("• Spare mehr Eigenkapital an (Ziel: mindestens 20%)")
    st.write("• Prüfe staatliche Förderungen (KfW, Baukindergeld, etc.)")

st.write("• Hole mehrere Finanzierungsangebote ein")
st.write("• Kalkuliere einen Puffer für Reparaturen und Instandhaltung ein")
st.write("• Berücksichtige auch laufende Kosten (Strom, Heizung, Versicherungen)")