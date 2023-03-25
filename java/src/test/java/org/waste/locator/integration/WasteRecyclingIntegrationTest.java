package org.waste.locator.integration;

import static io.restassured.RestAssured.given;
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.junit4.SpringRunner;
import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.service.WasteTypeService;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
public class WasteRecyclingIntegrationTest {
	@LocalServerPort
    private int port;
    private final String coordinates = "57.548142,68.154844";

    @Test
    public void shouldReturnGlasCollectionPoint() {
        String result = callService("glass", coordinates);

        assertThat("Altglas - Adresse: Telephonweg neben 412; 22. Bezirk").isEqualTo(result);
    }

    @Test
    public void shouldReturnGlasCollectionPointNagarroClosest() {
        String result = callService("glass", "48.17111801511212 16.332124234017812");

        assertThat("Altglas - Adresse: Wagenseilgasse neben 5; 12. Bezirk").isEqualTo(result);
    }

    private String callService(String wasteType, String coordinates) {
        return given()
                .when()
                .get(createURLWithPort("/waste/v1/" + wasteType+"/" + coordinates))
                .then()
                .statusCode(200)
                .extract()
                .asString();
    }

    @Test
    public void shouldReturnPlasticlCollectionPoint() {
        String result = callService("plastic", coordinates);

        assertThat("Gelbe Tonne - Adresse: Telephonweg neben 412; 22. Bezirk").isEqualTo(result);
    }

    @Test
    public void shouldReturnPaperCollectionPoint() {
        String result = callService("paper", coordinates);

        assertThat("Altpapier - Adresse: Telephonweg neben 412; 22. Bezirk").isEqualTo(result);
    }

    @Test
    public void shouldReturnMetallCollectionPoint() {
        String result = callService("metal", coordinates);

        assertThat("Gelbe Tonne - Adresse: Telephonweg neben 412; 22. Bezirk").isEqualTo(result);
    }

    @Test
    public void calcualteNearest(){
        WasteTypeService waste = new WasteTypeService();

        CollectionPoint collectionPoint = waste.calculateNearestCollectionPoint("48.17111801511212 16.332124234017812", "plastic");
        assertThat(collectionPoint).isNotNull();
        assertThat(collectionPoint.getAddress()).isEqualTo("Cothmannstraße neben 1; 12. Bezirk");
    }

    private String createURLWithPort(String uri) {
        return "http://localhost:" + port + uri;
    }
}
