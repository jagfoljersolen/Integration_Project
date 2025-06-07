from django.db import models

class Conflict(models.Model):
    TYPE_CHOICES = (
    (1, 'Type 1'),
    (2, 'Type 2'), 
    (3, 'Type 3'),
    (4, 'Type 4'),
    )
    conflict_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255)
    side_a = models.CharField(max_length=255)
    side_a_id = models.IntegerField()
    side_a_2nd = models.CharField(max_length=1024, blank=True, null=True)
    side_b = models.CharField(max_length=1024)
    side_b_id = models.CharField(max_length=1024)
    side_b_2nd = models.CharField(max_length=1024, blank=True, null=True)
    territory_name = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField()
    intensity_level = models.IntegerField()
    cumulative_intensity = models.IntegerField()
    type_of_conflict = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    start_date2 = models.DateField(blank=True, null=True)
    start_prec2 = models.IntegerField(blank=True, null=True)
    ep_end = models.IntegerField(blank=True, null=True)
    ep_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Conflict {self.side_a} - {self.side_b} ({self.year})"



class Commodity(models.Model):
    year = models.IntegerField(primary_key=True, verbose_name="Year")
    
    # Energy commodities with units
    crude_oil_average_bbl = models.FloatField(null=True, blank=True, verbose_name="Crude Oil Average ($/bbl)")
    crude_oil_brent_bbl = models.FloatField(null=True, blank=True, verbose_name="Crude Oil Brent ($/bbl)")
    crude_oil_dubai_bbl = models.FloatField(null=True, blank=True, verbose_name="Crude Oil Dubai ($/bbl)")
    crude_oil_wti_bbl = models.FloatField(null=True, blank=True, verbose_name="Crude Oil WTI ($/bbl)")
    
    # Coal with units
    coal_australian_mt = models.FloatField(null=True, blank=True, verbose_name="Coal Australian ($/mt)")
    coal_south_african_mt = models.FloatField(null=True, blank=True, verbose_name="Coal South African ($/mt)")
    
    # Natural gas with units
    natural_gas_us_mmbtu = models.FloatField(null=True, blank=True, verbose_name="Natural Gas US ($/mmbtu)")
    natural_gas_europe_mmbtu = models.FloatField(null=True, blank=True, verbose_name="Natural Gas Europe ($/mmbtu)")
    liquefied_natural_gas_japan_mmbtu = models.FloatField(null=True, blank=True, verbose_name="Liquefied Natural Gas Japan ($/mmbtu)")
    natural_gas_index_2010_100 = models.FloatField(null=True, blank=True, verbose_name="Natural Gas Index (2010=100)")
    
    # Agricultural commodities - Beverages
    cocoa = models.FloatField(null=True, blank=True, verbose_name="Cocoa ($/kg)")
    coffee_arabica_kg = models.FloatField(null=True, blank=True, verbose_name="Coffee Arabica ($/kg)")
    coffee_robusta_kg = models.FloatField(null=True, blank=True, verbose_name="Coffee Robusta ($/kg)")
    tea_avg_3_auctions_kg = models.FloatField(null=True, blank=True, verbose_name="Tea Avg 3 Auctions ($/kg)")
    tea_colombo_kg = models.FloatField(null=True, blank=True, verbose_name="Tea Colombo ($/kg)")
    tea_kolkata_kg = models.FloatField(null=True, blank=True, verbose_name="Tea Kolkata ($/kg)")
    tea_mombasa_kg = models.FloatField(null=True, blank=True, verbose_name="Tea Mombasa ($/kg)")
    
    # Oils and meals
    coconut_oil_mt = models.FloatField(null=True, blank=True, verbose_name="Coconut Oil ($/mt)")
    groundnuts_mt = models.FloatField(null=True, blank=True, verbose_name="Groundnuts ($/mt)")
    fish_meal_mt = models.FloatField(null=True, blank=True, verbose_name="Fish Meal ($/mt)")
    groundnut_oil_mt = models.FloatField(null=True, blank=True, verbose_name="Groundnut Oil ($/mt)")
    palm_oil_mt = models.FloatField(null=True, blank=True, verbose_name="Palm Oil ($/mt)")
    palm_kernel_oil_mt = models.FloatField(null=True, blank=True, verbose_name="Palm Kernel Oil ($/mt)")
    soybeans_mt = models.FloatField(null=True, blank=True, verbose_name="Soybeans ($/mt)")
    soybean_oil_mt = models.FloatField(null=True, blank=True, verbose_name="Soybean Oil ($/mt)")
    soybean_meal_mt = models.FloatField(null=True, blank=True, verbose_name="Soybean Meal ($/mt)")
    
    # Grains
    barley_mt = models.FloatField(null=True, blank=True, verbose_name="Barley ($/mt)")
    maize_mt = models.FloatField(null=True, blank=True, verbose_name="Maize ($/mt)")
    sorghum_mt = models.FloatField(null=True, blank=True, verbose_name="Sorghum ($/mt)")
    rice_thai_5_mt = models.FloatField(null=True, blank=True, verbose_name="Rice Thai 5 ($/mt)")
    rice_thai_25_mt = models.FloatField(null=True, blank=True, verbose_name="Rice Thai 25 ($/mt)")
    rice_thai_a_1_mt = models.FloatField(null=True, blank=True, verbose_name="Rice Thai A 1 ($/mt)")
    rice_vietnamese_5_mt = models.FloatField(null=True, blank=True, verbose_name="Rice Vietnamese 5 ($/mt)")
    wheat_us_srw_mt = models.FloatField(null=True, blank=True, verbose_name="Wheat US SRW ($/mt)")
    wheat_us_hrw_mt = models.FloatField(null=True, blank=True, verbose_name="Wheat US HRW ($/mt)")
    
    # Other food
    banana_europe_kg = models.FloatField(null=True, blank=True, verbose_name="Banana Europe ($/kg)")
    banana_us_kg = models.FloatField(null=True, blank=True, verbose_name="Banana US ($/kg)")
    orange_kg = models.FloatField(null=True, blank=True, verbose_name="Orange ($/kg)")
    beef_kg = models.FloatField(null=True, blank=True, verbose_name="Beef ($/kg)")
    chicken_kg = models.FloatField(null=True, blank=True, verbose_name="Chicken ($/kg)")
    lamb_kg = models.FloatField(null=True, blank=True, verbose_name="Lamb ($/kg)")
    shrimps_mexican_kg = models.FloatField(null=True, blank=True, verbose_name="Shrimps Mexican ($/kg)")
    sugar_eu_kg = models.FloatField(null=True, blank=True, verbose_name="Sugar EU ($/kg)")
    sugar_us_kg = models.FloatField(null=True, blank=True, verbose_name="Sugar US ($/kg)")
    sugar_world_kg = models.FloatField(null=True, blank=True, verbose_name="Sugar World ($/kg)")
    
    # Raw materials
    tobacco_us_import_uv_mt = models.FloatField(null=True, blank=True, verbose_name="Tobacco US Import UV ($/mt)")
    logs_cameroon_cubic_meter = models.FloatField(null=True, blank=True, verbose_name="Logs Cameroon ($/cubic meter)")
    logs_malaysian_cubic_meter = models.FloatField(null=True, blank=True, verbose_name="Logs Malaysian ($/cubic meter)")
    sawnwood_cameroon_cubic_meter = models.FloatField(null=True, blank=True, verbose_name="Sawnwood Cameroon ($/cubic meter)")
    sawnwood_malaysian_cubic_meter = models.FloatField(null=True, blank=True, verbose_name="Sawnwood Malaysian ($/cubic meter)")
    plywood_sheet = models.FloatField(null=True, blank=True, verbose_name="Plywood (¢/sheet)")
    cotton_a_index_kg = models.FloatField(null=True, blank=True, verbose_name="Cotton A Index ($/kg)")
    rubber_tsr20_kg = models.FloatField(null=True, blank=True, verbose_name="Rubber TSR20 ($/kg)")
    rubber_rss3_kg = models.FloatField(null=True, blank=True, verbose_name="Rubber RSS3 ($/kg)")
    
    # Fertilizers
    phosphate_rock_mt = models.FloatField(null=True, blank=True, verbose_name="Phosphate Rock ($/mt)")
    dap_mt = models.FloatField(null=True, blank=True, verbose_name="DAP ($/mt)")
    tsp_mt = models.FloatField(null=True, blank=True, verbose_name="TSP ($/mt)")
    urea_mt = models.FloatField(null=True, blank=True, verbose_name="Urea ($/mt)")
    potassium_chloride_mt = models.FloatField(null=True, blank=True, verbose_name="Potassium Chloride ($/mt)")
    
    # Metals and minerals
    aluminum_mt = models.FloatField(null=True, blank=True, verbose_name="Aluminum ($/mt)")
    iron_ore_cfr_spot_mt = models.FloatField(null=True, blank=True, verbose_name="Iron Ore CFR Spot ($/mt)")
    copper_mt = models.FloatField(null=True, blank=True, verbose_name="Copper ($/mt)")
    lead_mt = models.FloatField(null=True, blank=True, verbose_name="Lead ($/mt)")
    tin_mt = models.FloatField(null=True, blank=True, verbose_name="Tin ($/mt)")
    nickel_mt = models.FloatField(null=True, blank=True, verbose_name="Nickel ($/mt)")
    zinc_mt = models.FloatField(null=True, blank=True, verbose_name="Zinc ($/mt)")
    
    # Precious metals
    gold_troy_oz = models.FloatField(null=True, blank=True, verbose_name="Gold ($/troy oz)")
    platinum_troy_oz = models.FloatField(null=True, blank=True, verbose_name="Platinum ($/troy oz)")
    silver_troy_oz = models.FloatField(null=True, blank=True, verbose_name="Silver ($/troy oz)")

    def __str__(self):
        return f"Commodity Data for Year {self.year}"
    
    class Meta:
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"
