fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["date"], df["EU_Price_Super95"], label="EU Petrol")
ax.plot(df["date"], df["AT_Price_Super95"], label="Austria Petrol")
ax.plot(df["date"], df["DE_Price_Super95"], label="Germany Petrol")

ax.set_title("Petrol Prices Comparison (EU vs AT vs DE)")
ax.legend()

ax.grid(True, axis="y", alpha=0.2)
sns.despine(ax=ax)

plt.xticks(rotation=30)
plt.tight_layout()
