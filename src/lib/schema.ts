import { SITE_URL } from './site';

interface Crumb { name: string; url: string }
interface Faq { question: string; answer: string }

interface CityServiceSchemaInput {
  pageUrl: string;
  breadcrumbs: Crumb[];
  name: string;
  serviceType: string;
  description: string;
  areaName: string;
  pricing: { small: number; medium: number; large: number };
  tierNames: [string, string, string];
  faqs?: Faq[];
  inLanguage: string;
}

/**
 * JSON-LD for a "service × city" page.
 *
 * Uses `Service` with the Organization as provider instead of a per-city
 * `LocalBusiness`: the platform has no verified premises, phone number or
 * review data per city, so no address, telephone or aggregateRating is emitted.
 */
export function cityServiceSchema(input: CityServiceSchemaInput) {
  const { pageUrl } = input;
  const graph: object[] = [
    {
      '@type': 'BreadcrumbList',
      '@id': `${pageUrl}#breadcrumb`,
      itemListElement: input.breadcrumbs.map((c, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        name: c.name,
        item: c.url,
      })),
    },
    {
      '@type': 'Service',
      '@id': `${pageUrl}#service`,
      name: input.name,
      serviceType: input.serviceType,
      description: input.description,
      url: pageUrl,
      inLanguage: input.inLanguage,
      provider: { '@id': `${SITE_URL}/#organization` },
      areaServed: { '@type': 'City', name: input.areaName },
      offers: input.tierNames.map((tier, i) => ({
        '@type': 'Offer',
        name: tier,
        priceCurrency: 'GBP',
        priceSpecification: {
          '@type': 'PriceSpecification',
          minPrice: [input.pricing.small, input.pricing.medium, input.pricing.large][i],
          priceCurrency: 'GBP',
        },
      })),
    },
  ];
  if (input.faqs && input.faqs.length > 0) {
    graph.push({
      '@type': 'FAQPage',
      '@id': `${pageUrl}#faq`,
      mainEntity: input.faqs.map((faq) => ({
        '@type': 'Question',
        name: faq.question,
        acceptedAnswer: { '@type': 'Answer', text: faq.answer },
      })),
    });
  }
  return { '@context': 'https://schema.org', '@graph': graph };
}
