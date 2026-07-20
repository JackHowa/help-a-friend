import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'One-command recon',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Run <code>recon_check.py their-domain.org</code> and get a full
        markdown report: cloaking, Safe Browsing, WordPress exposure,
        security headers, SSL, DNS, and subdomain takeover risks.
      </>
    ),
  },
  {
    title: 'Built for volunteers, not vendors',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Zero-dependency stdlib Python, gitignored per-engagement findings,
        and fill-in-the-blank templates — designed for a one-hour volunteer
        call, reusable across every nonprofit you help next.
      </>
    ),
  },
  {
    title: 'Recovery, not just diagnosis',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Beyond detection: a reconsideration-request draft, a recovery
        playbook, and an image optimizer to fix what PageSpeed flags —
        everything you need to hand the org a finished plan.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
