def main():
    total_value = 100
    country = "AU"

    if country == "US":
        if total <= 50:
            print "Shipping cost is $50."
        elif total <= 100:
            print "Shipping cost is $25."
        elif total <= 150:
            print "Shipping costs is $5."
        else:
            print "It is free."

    country = "AU"
    if total <= 50:
        print "Shipping cost is $100."
    else:
        print "It is free."

main()
