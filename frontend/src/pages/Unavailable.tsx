import { CapabilityUnavailable } from '../components/common';

export default function Unavailable({
  title,
  module,
  detail,
}: {
  title: string;
  module: string;
  detail: string;
}) {
  return <CapabilityUnavailable module={module} title={title} detail={detail} />;
}
