# -*- coding: utf-8 -*-

# Documentation:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LaptopsdirectItem(scrapy.Item):
    # Primary Fields
    sku = scrapy.Field()
    sku2 = scrapy.Field()
    sku3 = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    europrice = scrapy.Field()
    product_title = scrapy.Field()
    description = scrapy.Field()
    stock = scrapy.Field()
    availability = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    image_srcx = scrapy.Field()
    dburls = scrapy.Field()
    category = scrapy.Field()
    ean = scrapy.Field()
    meta = scrapy.Field()

    #Mobile Phone Scrape Fields

    numberofdeals = scrapy.Field()
    recycler = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()

    #attribute Scrape
    slotsqty = scrapy.Field()
    emptyslots = scrapy.Field()
    imagebrightness = scrapy.Field()
    #TelevisionDiagonalClass = scrapy.Field()
    TelevisionDiagonalSize = scrapy.Field()
    #TelevisionCommercialUse = scrapy.Field()
    #TvTunerTvTunerPresence = scrapy.Field()
    #TvTunerTvTunerPresence2 = scrapy.Field()
    #TelevisionVideoInterface = scrapy.Field()
    #TelevisionHDMIPortsqty = scrapy.Field()
    #PcInterface = scrapy.Field()
    #Dimensionswidth = scrapy.Field()
    #Dimensionsdepth = scrapy.Field()
    #Dimensionsheight = scrapy.Field()
    #TelevisionResolution = scrapy.Field()
    TelevisionDisplayFormat = scrapy.Field()
    #TelevisionImageAspectRatio = scrapy.Field()
    #TelevisionLCDBacklightTechnology = scrapy.Field()
    #TelevisionImageContrastRatio = scrapy.Field()
    #TelevisionBrightness = scrapy.Field()
    #TelevisionViewingAngle = scrapy.Field()
    #TelevisionResponseTime = scrapy.Field()
    #VesaMountingInterfaces = scrapy.Field()
    #UsbPort = scrapy.Field()
    #AudioSystemSpeakerSystem = scrapy.Field()
    #Networkstreamingservices = scrapy.Field()
    #NetworkConnectivity = scrapy.Field()
    #Cablesincluded = scrapy.Field()
    #Tiltangle = scrapy.Field()
    #AudioOutput = scrapy.Field()
    #Paneltype = scrapy.Field()
    TelevisionType = scrapy.Field()
    TVTunerDigitalTVTuner = scrapy.Field()
    TelevisionHDR10 = scrapy.Field()

    #Additional Scrape Fields
    pcwb_product_code = scrapy.Field()
    processor = scrapy.Field()
    processormodel = scrapy.Field()
    ram = scrapy.Field()
    harddrive = scrapy.Field()
    html = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    breadcrumb = scrapy.Field()

    #Monitored Attribute
    monitoredcategory = scrapy.Field()
    monitoredattribute = scrapy.Field()
    monitoredattribute2 = scrapy.Field()

    # Administration Fields
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    ip = scrapy.Field()
    date = scrapy.Field()
    useragent = scrapy.Field()

class BookItem(scrapy.Item):
    #other fields...
    images = scrapy.Field()
    image_urls = scrapy.Field()

class MobilePhoneItem(scrapy.Item):

    # Primary Fields
    sku = scrapy.Field()
    sku2 = scrapy.Field()
    sku3 = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    product_title = scrapy.Field()
    description = scrapy.Field()
    stock = scrapy.Field()
    availability = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    dburls = scrapy.Field()
    category = scrapy.Field()

    #Mobile Phone Scrape Fields

    numberofdeals = scrapy.Field()
    recycler = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()

    #Additional Scrape Fields
    pcwb_product_code = scrapy.Field()
    processor = scrapy.Field()
    processormodel = scrapy.Field()
    ram = scrapy.Field()
    harddrive = scrapy.Field()
    html = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

    #Monitored Attributes
    monitoredcategory = scrapy.Field()
    monitoredattribute = scrapy.Field()
    monitoredattribute2 = scrapy.Field()

    # Administration Fields
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    date = scrapy.Field()
    useragent = scrapy.Field()