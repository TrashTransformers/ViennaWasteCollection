package org.waste.locator.model;

public record WasteCollectionPointResponse(double xCoordinates, double yCoordinates, String adresse,
                                           String typeOfDisposal) {

    public double getxCoordinates() {
        return xCoordinates;
    }

    public double getyCoordinates() {
        return yCoordinates;
    }

    public String getAdresse() {
        return adresse;
    }

    public String getTypeOfDisposal() {
        return typeOfDisposal;
    }
}
