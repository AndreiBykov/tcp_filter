#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

#define ETH_IPv4 0x0800
#define IP_TCP 	6

int tcp_filter(struct __sk_buff *skb) { 
	u8 *cursor = 0;	

	struct ethernet_t *ethernet = cursor_advance(cursor, sizeof(*ethernet));
	
	if(ethernet->type != ETH_IPv4) {
	    	goto DROP;
	}

	struct ip_t *ip = cursor_advance(cursor, sizeof(*ip));
	if (ip->nextp != IP_TCP) {
		goto DROP;
	}

	struct tcp_t *tcp = cursor_advance(cursor, sizeof(*tcp));
	if (tcp->dst_port != 80 && tcp->dst_port != 443) {
		goto DROP;
	}

	KEEP:
		return -1;

	DROP:
		return 0;
}
