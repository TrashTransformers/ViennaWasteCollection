package org.waste.locator.model;

import com.fasterxml.jackson.annotation.JsonAlias;

public record WasteCollectionPointResponse(double longitude, double latitude, String address,
                                           String typeOfDisposal) {

    @JsonAlias("longitude")
    public double getLongitude() {
        return longitude;
    }

    @JsonAlias("latitude")
    public double getLatitude() {
        return latitude;
    }

    @JsonAlias("address")
    public String getAddress() {
        return address;
    }

    @JsonAlias("typeOfDisposal")
    public String getTypeOfDisposal() {
        return typeOfDisposal;
    }
}
