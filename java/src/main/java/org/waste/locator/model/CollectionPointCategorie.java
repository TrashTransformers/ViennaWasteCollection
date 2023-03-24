package org.waste.locator.model;

public enum CollectionPointCategorie {
    PLASTIC("Gelbe Tonne"),
    GLASS("Altglas"),
    PAPER("Altpapier"),
    BIOMUELL("Biom\u00FCll"),
    MISTPLATZ("Mistplatz"),
    PROBLEMSTOFF("Problemstoff");

    private String description;

    CollectionPointCategorie(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
