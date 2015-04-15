from pprint import pprint

import stix
import stix.core.stix_package

import capnp

print('pycapnp version: {}'.format(capnp.__version__))
print('pystix version: {}'.format(stix.__version__))
print('')


capnp.remove_import_hook()
stix_capnp = capnp.load('stix.capnp')

print('stix.capnp schema version: {0}'.format(stix_capnp.version))
print('')


def xml_to_obj(path='sample.xml'):
    parsed_package = stix.core.stix_package.STIXPackage.from_xml(path)
    return parsed_package


def obj_to_capnp(dict_package):
    stix_package = stix_capnp.STIXPackage.new_message()
    stix_package.id = dict_package['id']
    stix_package.timestamp = dict_package['timestamp']
    stix_package.version = dict_package['version']

    stix_package.stixHeader = stix_capnp.STIXHeader.new_message(
        title=dict_package['stix_header']['title'] if 'title' in dict_package['stix_header'] else '',
        description=dict_package['stix_header']['description'] if 'description' in dict_package['stix_header'] else '',
        informationSource=stix_capnp.STIXHeader.InformationSource.new_message(
            time=stix_capnp.STIXHeader.InformationSource.Time.new_message(
                producedTime=dict_package['stix_header']['information_source']['time']['produced_time']
            )
        )
    )

    if 'package_intents' in dict_package['stix_header']:
        package_intents = stix_package.stixHeader.init('packageIntents', len(dict_package['stix_header']['package_intents']))
        for iintent, package_intent in enumerate(dict_package['stix_header']['package_intents']):
            stix_intent = stix_capnp.PackageIntent.new_message(
                value=package_intent['value'],
                type=package_intent['xsi:type']
            )
            package_intents[iintent] = stix_intent

    indicators = stix_package.init('indicators', len(dict_package['indicators']))

    for idx, indicator in enumerate(dict_package['indicators']):
        stix_indicator = stix_capnp.Indicator.new_message(
            id=indicator['id'],
            timestamp=indicator['timestamp'],
            description=indicator['description'] if 'description' in indicator else '',
            shortDescription=indicator['short_description'] if 'short_description' in indicator else '',
            title=indicator['title'] if 'title' in indicator else '',
            version=indicator['version'] if 'version' in indicator else '',
            likelyImpact=stix_capnp.Indicator.LikelyImpact.new_message(
                description=indicator['likely_impact']['description'] if 'description' in indicator['likely_impact'] else '',
                value=indicator['likely_impact']['value'] if 'value' in indicator['likely_impact'] else ''
            ) if 'likely_impact' in indicator else '',
            producer=stix_capnp.Indicator.Producer.new_message() if 'producer' in indicator else '',
            confidence=stix_capnp.Indicator.Confidence.new_message(
                timestamp=indicator['confidence']['timestamp'] if 'timestamp' in indicator['confidence'] else '',
                value=stix_capnp.Indicator.Confidence.ConfidenceValue.new_message(
                    value=indicator['confidence']['value']['value'] if 'value' in indicator['confidence']['value'] else '',
                    type=indicator['confidence']['value']['xsi:type'] if 'xsi:type' in indicator['confidence']['value'] else '',
                ) if 'value' in indicator['confidence'] else '',
            ) if 'confidence' in indicator else ''
        )

        if 'producer' in indicator:
            stix_indicator.producer.init('tools', len(indicator['producer']['tools']))
            for tid, tool in enumerate(indicator['producer']['tools']):
                stix_tool = stix_capnp.Indicator.Producer.Tool.new_message(
                    description=tool['description'],
                    name=tool['name'],
                    vendor=tool['vendor'],
                    version=tool['version']
                )
                stix_indicator.producer.tools[tid] = stix_tool

        indicator_types = stix_indicator.init('indicatorTypes', len(indicator['indicator_types']))
        for iidx, indicator_type in enumerate(indicator['indicator_types']):
            if isinstance(indicator_type, str):
                indicator_types[iidx] = stix_capnp.IndicatorType.new_message(
                    value=indicator_type
                )
            else:
                indicator_types[iidx] = stix_capnp.IndicatorType.new_message(
                    value=indicator_type['value'],
                    type=indicator_type['xsi:type']
                )
        if 'observable' in indicator:
            stix_indicator.observable = stix_capnp.Observable.new_message(
                id=indicator['observable']['id'],
                object=stix_capnp.Observable.ObservableObject.new_message(
                    id=indicator['observable']['object']['id'],
                    properties=stix_capnp.IPWatchlist.new_message(
                        addressValue=stix_capnp.IPWatchlist.Watchlist.new_message(
                            applyCondition=indicator['observable']['object']['properties']['address_value']['apply_condition'],
                            condition=indicator['observable']['object']['properties']['address_value']['condition'],
                            value=indicator['observable']['object']['properties']['address_value']['value']
                        ),
                        category=indicator['observable']['object']['properties']['category'],
                        type=indicator['observable']['object']['properties']['xsi:type']
                    )
                )
            )

        if 'related_indicators' in indicator:
            related_indicators = indicator['related_indicators']['related_indicators']
            stix_indicator.relatedIndicators = stix_capnp.Indicator.RelatedIndicators.new_message()
            stix_indicator.relatedIndicators.init('relatedIndicators', len(related_indicators))
            for rix, related_indicator in enumerate(related_indicators):
                related_indicator = related_indicator['indicator']
                related_stix_indicator = stix_capnp.Indicator.RelatedIndicators.RelatedIndicator.new_message(
                    indicator=stix_capnp.Indicator.new_message(
                        id=related_indicator['id'],
                        timestamp=related_indicator['timestamp'],
                        description=related_indicator['description'] if 'description' in related_indicator else '',
                        shortDescription=related_indicator['short_description'] if 'short_description' in related_indicator else '',
                        title=related_indicator['title'] if 'title' in related_indicator else '',
                        version=related_indicator['version'] if 'version' in related_indicator else '',
                        likelyImpact=stix_capnp.Indicator.LikelyImpact.new_message(
                            description=related_indicator['likely_impact']['description'],
                            value=related_indicator['likely_impact']['value']
                        ) if 'likely_impact' in related_indicator else stix_capnp.Indicator.LikelyImpact.new_message(),
                        confidence=stix_capnp.Indicator.Confidence.new_message(
                            timestamp=related_indicator['confidence']['timestamp'],
                            value=stix_capnp.Indicator.Confidence.ConfidenceValue.new_message(
                                value=related_indicator['confidence']['value']['value'],
                                type=related_indicator['confidence']['value']['xsi:type']
                            )
                        ) if 'confidence' in related_indicator else stix_capnp.Indicator.Confidence.new_message(),
                    )
                )
                if 'indicator_types' in related_indicator:
                    related_indicator_types = related_indicator.init('indicatorTypes', len(related_indicator['indicator_types']))
                    for idz, indicator_type in enumerate(related_indicator['indicator_types']):
                        related_indicator_types[idz] = indicator_type
                stix_indicator.relatedIndicators.relatedIndicators[rix] = related_stix_indicator

        indicators[idx] = stix_indicator
    return stix_package


fuggly_mapping = dict(
    addressValue='address_value',
    applyCondition='apply_condition',
    indicatorTypes='indicator_types',
    informationSource='information_source',
    likelyImpact='likely_impact',
    packageIntents='package_intents',
    producedTime='produced_time',
    relatedIndicators='related_indicators',
    shortDescription='short_description',
    stixHeader='stix_header',
    type='xsi:type'
)


def recurse_fix(d):
    fixed = dict()
    if isinstance(d, dict):
        for k in d:
            if k in fuggly_mapping:
                d[fuggly_mapping[k]] = d.pop(k)
                k = fuggly_mapping[k]
            fixed[k] = recurse_fix(d[k])
    elif isinstance(d, list):
        fixed = list()
        for k in d:
            fixed.append(recurse_fix(k))
    else:
        fixed = d
    return fixed


if __name__ == '__main__':
    xml_obj = xml_to_obj('maa.xml')
    pprint(xml_obj.to_dict())
    ret = obj_to_capnp(xml_obj.to_dict())

    with open('ma_report.bin', 'w+b') as fh:
        ret.write(fh)

    print '+++++++++++++++++++++++++++++++++++++++++'

    ret = recurse_fix(ret.to_dict())
    # Show the output
    pprint(ret)
    # Make sure the package parse back into STIX
    xml_ret = stix.core.stix_package.STIXPackage.from_dict(ret).to_xml()
    print(len(xml_ret))
