import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`${siteConfig.title}`}
      description={siteConfig.tagline}
    >
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro"
            >
              🚀 Get Started
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <Feature
                title="TypeScript-First"
                description="Docusaurus 3 supports TypeScript configs and pages out of the box for maximum safety and DX."
              />
              <Feature
                title="Fast & Modern"
                description="Powered by React and MDX — author once, deploy everywhere."
              />
              <Feature
                title="Zero-Ops Deploy"
                description="Integrates seamlessly with GitHub Actions for automated build and deploy."
              />
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}

interface FeatureProps {
  title: string;
  description: string;
}

function Feature({ title, description }: FeatureProps): JSX.Element {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className="text--center">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}
