import { mount } from '@vue/test-utils';
import BottleListings from '../../src/views/Producers/BottleListings.vue';


// COMMAND TO RUN TEST: npm run test:unit

// -------------------------------------------------------------------------------------------------------------------------------------------------

// -- [TGB-7] WHERE TO BUY --
describe('Where To Buy', () => {
    // Sample listings data
    const all_listings = [
        {
            "_id":{"$oid":"65ad1b67ce3fc2aff52a874b"},
            "Expression Name":"Harmony Collection Inspired by Intense Arabica",
            "Producer":"The Macallan Distillery",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"Scotland",
            "Drink Type":"Whiskey / Whisky",
            "Drink Category":"Single Malt",
            "Age":"NAS",
            "ABV":"44%",
            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/whisky-reviews/the-macallan-harmony-collection-inspired-by-intense-arabica-single-malt-44-abv",
            "Official Description":"The second edition in our limited annual release series, this special single malt exudes flavours of sweet oak, tiramisu and dark chocolate, and provides a delightful whisky and coffee pairing experience."
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9f69"},
            "Expression Name":"Nikka From The Barrel",
            "Producer":"Nikka Whisky",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"Japan",
            "Drink Type":"Whiskey / Whisky",
            "Drink Category":"Blended",
            "Age":"NAS",
            "ABV":"51%",
            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/whisky-reviews/nikka-from-the-barrel",
            "Official Description":"This strong Japanese blend aged in bourbon barrels comes from the blend of two Nikka single malts Miyagikyo and Yoichi and a single grain whisky. Nikka from the Barrel was chosen best Japanese blended whisky under 12 years old at the World Whiskies Awards 2007."
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9f6a"},
            "Expression Name":"Ardbeg Ardcore",
            "Producer":"Ardbeg Distillery",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"Scotland",
            "Drink Type":"Whiskey / Whisky",
            "Drink Category":"Single Malt",
            "Age":"NAS",
            "ABV":"46%",
            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/whisky-reviews/ardbeg-ardcore-46-abv",
            "Official Description":"From a Distillery with more ups and downs that a pogoing punk comes Ardcore. Created with roasted black malt, roasted to the extreme, this spirit is all about what happens up front & centre stage. The malt is what defines its distinctive profile. Described as tasting like ‘biting on a spiky ball’, Ardcore is a dram that wears its heart on its sleeve… its black heart!"
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9fb7"},
            "Expression Name":"Clase Azul Tequila Reposado",
            "Producer":"Clase Azul",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"Mexico",
            "Drink Type":"Tequila",
            "Drink Category":"Reposado",
            "Age":"",
            "ABV":"40%",
            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/tequila-mezcal-reviews/clase-azul-tequila-reposado-40-abv",
            "Official Description":""
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9fbb"},
            "Expression Name":"Tequila Tapatio Excelencia Extra Anejo",
            "Producer":"Tapatio",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"Mexico",
            "Drink Type":"Tequila",
            "Drink Category":"Extra Anejo",
            "Age":"",
            "ABV":"40%",
            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/tequila-mezcal-reviews/tequila-tapatio-excelencia-extra-anejo",
            "Official Description":""
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9f7f"},
            "Expression Name":"Fords Gin",
            "Producer":"Fords Gin",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"United Kingdom",
            "Drink Type":"Gin",
            "Drink Category":"London Dry / Classic",
            "Age":"",
            "ABV":"45%",
            "88B Website Review (if applicable)":"",
            "Official Description":"Fords Gin is found in the very best gin joints around the world, from iconic hotel bars to frequently visited neighborhood spots. Created with respect to the traditions that have historically defined gin making, this classic London Dry is keen for all your cocktail adventures."
        },
        {
            "_id":{"$oid":"65ab760933b616ccc14b9f80"},
            "Expression Name":"Fords Gin Officers' Reserve",
            "Producer":"Fords Gin",
            "Bottler (OB or Specify name of IB)":"OB",
            "Country of Origin":"United Kingdom",
            "Drink Type":"Gin",
            "Drink Category":"London Dry / Classic",
            "Age":"",
            "ABV":"55%",
            "88B Website Review (if applicable)":"",
            "Official Description":"Over-proof gin was traditionally reserved for officers of the British Royal Navy. Today, it’s for everyone! Fords Gin Officers’ Reserve is rested and aged in Amontillado Sherry casks for three weeks. Characteristics of the barrel’s wood shape the spirit’s flavour. It is then bottled at 54.5 ABV. This limited release is Fords Gin’s first Journey in Gin as a homage to the Navy Strength Gin category."
        }
    ];

    // Mock the fetchData method
    const fetchDataMock = jest.fn(() => Promise.resolve(all_listings));

    // Search for Producers based on specified listing
    it('[Listings returned] Search for Producers based on specified listing', () => {
        const wrapper = mount(BottleListings, {
            data() {
                return {
                    listings: all_listings,
                    specified_listing:  {
                                            "_id":{"$oid":"65ab760933b616ccc14b9f6a"},
                                            "Expression Name":"Ardbeg Ardcore",
                                            "Producer":"Ardbeg Distillery",
                                            "Bottler (OB or Specify name of IB)":"OB",
                                            "Country of Origin":"Scotland",
                                            "Drink Type":"Whiskey / Whisky",
                                            "Drink Category":"Single Malt",
                                            "Age":"NAS",
                                            "ABV":"46%",
                                            "88B Website Review (if applicable)":"https://88bamboo.co/blogs/whisky-reviews/ardbeg-ardcore-46-abv",
                                            "Official Description":"From a Distillery with more ups and downs that a pogoing punk comes Ardcore. Created with roasted black malt, roasted to the extreme, this spirit is all about what happens up front & centre stage. The malt is what defines its distinctive profile. Described as tasting like ‘biting on a spiky ball’, Ardcore is a dram that wears its heart on its sleeve… its black heart!"
                                        }
                };
            },
        });
        // Call the whereToBuy method
        wrapper.vm.whereToBuy();
        expect(wrapper.vm.producerListings).toEqual(["Ardbeg Distillery"]);
    });

    // Search for Producers that do not exist based on specified listing
    it('[No listings returned] Search for Producers that do not exist based on specified listing', () => {
        const wrapper = mount(BottleListings, {
            data() {
                return {
                    listings: all_listings,
                    specified_listing:  {
                                            "_id":{"$oid":"65ab760933b616ccc14b9f7b"},
                                            "Expression Name":"KI NO BI Kyoto Dry Gin",
                                            "Producer":"Kyoto Distillery",
                                            "Bottler (OB or Specify name of IB)":"OB",
                                            "Country of Origin":"Japan",
                                            "Drink Type":"Gin",
                                            "Drink Category":"Contemporary",
                                            "Age":"",
                                            "ABV":"46%",
                                            "88B Website Review (if applicable)":"",
                                            "Official Description":"KI NO BI (“The Beauty of the Seasons”) is inspired by tradition and is distilled, blended and bottled in Kyoto. Our gin is made in a recognisably dry style, but with a distinct Japanese accent. KI NO BI Kyoto Dry Gin is created with Japanese botanicals such as yellow yuzu from the north of Kyoto Prefecture, akamatsu wood chips (Japanese red pine), bamboo, gyokuro tea from the Uji region and green sanshō (Japanese peppercorn) berries."
                                        }
                };
            },
        });
        // Call the whereToBuy method
        wrapper.vm.whereToBuy();
        expect(wrapper.vm.producerListings).toEqual([]);
    });

});

// -------------------------------------------------------------------------------------------------------------------------------------------------