package org.waste.locator.entity;

import org.waste.locator.model.CollectionPointCategorie;
import org.waste.locator.model.Coordinates;

import java.util.ArrayList;
import java.util.List;

public class CollectionPoint {
    //Altstoff, Mistplatz, Problemstoff, LEICHTVERPACKUNG, Mistplatz
    private final List<CollectionPointCategorie> collectionPointCategorieList = new ArrayList<>();
    private String address;
    private Coordinates coordinates;

    public void addCollectionPointCategorie(CollectionPointCategorie collectionPointCategorie) {
        collectionPointCategorieList.add(collectionPointCategorie);
    }

    public List<CollectionPointCategorie> getCollectionPointCategorieList() {
        return collectionPointCategorieList;
    }

    public String getAddress() {
        return address;
    }

    public Coordinates getCoordinate() {
        return coordinates;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public void setCoordinates(Coordinates coordinates) {
        this.coordinates = coordinates;
    }
}
