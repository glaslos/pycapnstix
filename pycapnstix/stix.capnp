# stix.capnp
@0x9110f426d1e73d4c;

const version :Text = "1.1.1";
annotation realName(*) :Text;

struct IndicatorType {
    value @0 :Text;
    type @1 :Text;
}

struct IPWatchlist {
    addressValue @0 :Watchlist;

    struct Watchlist {
        applyCondition @0 :Text = "ANY" $realName("apply_condition");
        condition @1 :Text = "Equals";
        value @2 :List(Text);
    }

    category @1 :Text;
    type @2 :Text;
}

struct Observable {
    id @0 :Text;
    object @1 :ObservableObject;

    struct ObservableObject {
        id @0 :Text;
        properties @1 :IPWatchlist;
    }
}

struct Indicator {
    id @0 :Text;
    timestamp @1 :Text;
    description @2 :Text;
    indicatorTypes @3 :List(IndicatorType);
    observable @4 :Observable;
    relatedIndicators @5 :RelatedIndicators;

    struct RelatedIndicators {
        relatedIndicators @0 :List(RelatedIndicator);

        struct RelatedIndicator {
            indicator @0 :Indicator;
        }

    }

    shortDescription @6 :Text;
    title @7 :Text;
    version @8 :Text;
    likelyImpact @9 :LikelyImpact;

    struct LikelyImpact {
        description @0 :Text;
        value @1 :Text;
    }

    producer @10 :Producer;

    struct Producer {
        tools @0 :List(Tool);

        struct Tool {
            description @0 :Text;
            name @1 :Text;
            vendor @2 :Text;
            version @3 :Text;
        }

    }

    confidence @11 :Confidence;

    struct Confidence {
        timestamp @0 :Text;
        value @1 :ConfidenceValue;

        struct ConfidenceValue {
            value @0 :Text;
            type @1 :Text;
        }

    }

}

struct PackageIntent {
    value @0 :Text;
    type @1 :Text;
}

struct STIXHeader {
    title @0 :Text;
    description @1 :Text;
    packageIntents @2 :List(PackageIntent);
    informationSource @3 :InformationSource;

    struct InformationSource {
        time @0 :Time;

        struct Time {
            producedTime @0 :Text;
        }

    }

}

struct STIXPackage {
    id @0 :Text;
    timestamp @1 :Text;
    version @2 :Text;
    stixHeader @3 :STIXHeader;
    indicators @4 :List(Indicator);
}