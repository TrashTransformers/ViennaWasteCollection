package org.waste.locator.service;

import org.waste.locator.model.CollectionPointCategorie;

public class WasteMapper {

    public static CollectionPointCategorie getTypeFromInput(String disposalType) {
        switch (disposalType) {
            case "plastic":
            case "metall":
                return CollectionPointCategorie.PLASTIC;
            case "glass":
                return CollectionPointCategorie.GLASS;
            case "paper":
                return CollectionPointCategorie.PAPER;
        }
        throw new IllegalArgumentException("No Disposal Type can be mapped to parameter: " + disposalType);
    }
}
