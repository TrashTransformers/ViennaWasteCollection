package org.waste.locator.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.model.WasteCollectionPointResponse;
import org.waste.locator.service.WasteMapper;
import org.waste.locator.service.WasteTypeService;


@RestController
@RequestMapping("/waste")
public class WasteTypeController {
    @Autowired
    private WasteTypeService service;

    @GetMapping("/v1/{wasteType}/{currentCoordinates}")
    public WasteCollectionPointResponse calculateNearestCollectionPoint(
            @PathVariable String wasteType,
            @PathVariable String currentCoordinates) {
        CollectionPoint collectionPoint;
        try {
            collectionPoint = service.calculateNearestCollectionPoint(currentCoordinates, wasteType);
        } catch (Exception e) {
            throw new IllegalArgumentException("Error in Calculation with input " + currentCoordinates + "; " + wasteType + "\n" + e.getMessage());
        }
        return new WasteCollectionPointResponse(collectionPoint.getCoordinate().getX(),
                collectionPoint.getCoordinate().getY(),
                collectionPoint.getAddress(),
                WasteMapper.getTypeFromInput(wasteType).getDescription());
    }
}
